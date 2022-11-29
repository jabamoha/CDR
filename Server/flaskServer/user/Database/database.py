from pymongo import MongoClient
import os
import string
import random
import gridfs
import sys
import hashlib
sys.path.append(os.path.abspath('C:\\temp\\NAC\\FinalProject\\CDRFP\\CDRFinal\\Server\\flaskServer\\user\\Database'))#Database path
from Entities import *
# define a list to store all hashcodes in the 5 collections...
HashCodes = []


LETTERS = string.ascii_uppercase+string.ascii_lowercase+string.digits

class DataBase:
    DATABASE = "CDRDB"
    USERS = "users"
    FILES = "CDRFiles"
    LOGS = "logs"
    EMAILS = "emails"
    CONTENT = "content"
    
    def __init__(self):
        def _read_auth():
            for file in os.listdir('C:\\temp\\NAC\\FinalProject\\CDRFP\\CDRFinal\\Server\\flaskServer\\user\\Database\\auth'): #change path to auth directory 
                fp = open('C:\\temp\\NAC\\FinalProject\\CDRFP\\CDRFinal\\Server\\flaskServer\\user\\Database\\auth\\'+file,'r')
                yield fp.read().strip()
                fp.close()
        generator =_read_auth()
        password = next(generator)
        username = next(generator)
        uri =f"mongodb+srv://{username}:{password}@ecdr.tbxowkh.mongodb.net/?retryWrites=true&w=majority"
        self._client = MongoClient(uri)
        del uri,password,username,generator,_read_auth
        
        self._db = self._client[self.DATABASE]
        self._users = self._db[self.USERS]
        self._logs = self._db[self.LOGS]
        self._files = self._db[self.FILES]
        self._emails = self._db[self.EMAILS]
        self._content = self._db[self.CONTENT]
        self._fs = gridfs.GridFS(self._db)
        
        def fill_codes(col):
            docs = col.find({})            
            if not docs:
                HashCodes = set(HashCodes + [doc["hashcode"] for doc in docs]) 
        atts = [self._users,self._logs,self._files,self._emails,self._content]
        for o in atts:
            fill_codes(o)
        
        del fill_codes,atts



    def generate_hashcode(self):
        hashcode = ''.join(random.choice(LETTERS) for _ in range(32))
        
        if not hashcode in HashCodes:
            HashCodes.append(hashcode)
            return hashcode
        
        del hashcode
        self.generate_hashcode()
        
    
    
    def insert_user(self,email_address: str , password : str) -> bool:
        if  self._find_user(email_address=email_address) is None:
            salt = ''.join(random.choice(LETTERS) for _ in range(16))
            hashcode = self.generate_hashcode()
            hashpass = hashlib.sha256((password + salt).encode()) 
            self._users.insert_one({
                                User.EMAIL_ADDRESS : email_address ,
                                User.SALT : salt,
                                User.PASSWORD : hashpass,
                                User.CODE : hashcode
                                })
            del hashcode , salt , hashpass
            return True
        else:
            return False
    
            
    def _find_user(self,email_address : str):
        doc = self._users.find({User.EMAIL_ADDRESS:email_address})
        temp=list(doc)
        x=len(temp)
        print(x)
        if x != 0:
            print('test 11')
            return temp[0][User.CODE]
        
        return None
    
        
    def insert_file(self,filepath,content_code,filename) -> CDRFile :
        
        file_data = open(filepath,'rb')
        data = file_data.read()
        hashcode = self.generate_hashcode()
        file_id = self._fs.put(data ,code = hashcode)
        file_data.close()
        cdr_file = CDRFile(hashcode=hashcode,system_path=filepath,file_id=file_id,content_code=content_code,file_name=filename)
        self._files.insert_one(
                                {CDRFile.FILE_ID:file_id,
                                 CDRFile.CONTENT_CODE:content_code,
                                 CDRFile.CODE:hashcode,
                                 CDRFile.NAME:filename,
                                 CDRFile.SIZE:cdr_file._size,
                                 CDRFile.TYPE:cdr_file._type
                                 })
        
        del file_data,file_id,data,hashcode
        
        return cdr_file
        
        
    def get_file(self,file_id,download_location):
        output_data = self._fs.get(file_id)
        output_data.read()
        output = open(download_location,'wb')
        output.write(output_data)
        output.close()
        
        del output_data,output
    
    
    def insert_logs(self, logs:list[str] , file_id) ->Logs:
        
        hashcode = self.generate_hashcode()
        self._logs.insert_one({
                                Logs.FILE_ID:file_id,
                                Logs.LOGS:logs,
                                Logs.CODE:hashcode
        })
        
        file_logs = Logs(file_id=file_id , logs= logs , hashcode= hashcode)
        del hashcode
        return file_logs
        
    def get_logs(self,file_id):
        doc = self._logs.find_one({"file_id":file_id})
        if len(list(doc)) != 0 :
            return Logs(file_id=file_id , hashcode=doc[0]["code"] , logs=doc[0]["logs"])
        return None
        
    def insert_email_message(self,message:Message):
        hashcode = self.generate_hashcode()
        self._emails.insert_one({
                                Message.FROM : message._from,
                                Message.SUBJECT : message._subject,
                                Message.CC : message._cc,
                                Message.DATE : message._date,
                                Message.SECUIRTY : message.__security,
                                Message.MAILED_BY : message._mailedBy,
                                Message.SIGNED_BY : message._signedBy,
                                Message.CONTENT : message._content,
                                Message.TO : message._to,
                                Message.CODE : hashcode
        })
        del hashcode
        
    
    def get_email_message(self,message_code):
        doc = self._emails.find_one({"code":message_code})
        if len(list(doc)) != 0 :
            obj = doc[0]
            return Message(from_email=obj[Message.FROM],usercode=obj[Message.TO],
                           date= obj[Message.DATE],content=obj[Message.CONTENT],
                           hashcode=obj[Message.CODE],subject=obj[Message.SUBJECT],
                           cc=obj[Message.CC],security=obj[Message.SECUIRTY],
                           mailed_by=obj[Message.MAILED_BY],signed_by=obj[Message.SIGNED_BY])
        return None                        
    
    # content
    
    def insert_content(self,content:Content):
        hashcode = self.generate_hashcode()
        self._content.insert_one({
                                    Content.CODE:hashcode,
                                    Content.ATTACHMENTS:content._attachments,
                                    Content.MESSAGE_CODE:content._messageCode,
                                    Content.TEXT:content._text
        })
        
        del hashcode
    
    
    def get_content(self,message_Code:str):
        doc = self._content.find_one({Content.MESSAGE_CODE:message_Code})
        content = None
        if len(list(doc)) != 0 :
            content = Content(message_code = message_Code , hashcode=doc[0][Content.CODE],
                              text=doc[0][Content.TEXT], attachments=doc[0][Content.ATTACHMENTS])
        
        del doc
        return content
    
    
   