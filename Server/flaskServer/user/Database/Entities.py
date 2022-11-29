import os

class User:
    EMAIL_ADDRESS = "email_address"
    CODE = "code"
    SALT = "salt"
    PASSWORD = "password"
    def __init__(self , email_address , hashcode = None):
        self._email = email_address
        self._code = hashcode
        
class Message:
    FROM = "from"
    SUBJECT ="subject"
    CC = "cc"
    DATE = "date"
    SECUIRTY = "security"
    MAILED_BY = "mailedBy"
    SIGNED_BY = "signedBy"
    CONTENT = "content"
    TO = "to"
    CODE = "code" 
    def __init__(self, from_email , usercode, date ,content , hashcode =None, subject=None ,  cc=None  , security=None , mailed_by=None ,signed_by=None ):
        self._from = from_email
        self._subject = subject
        self._cc = cc
        self._date = date
        self._security = security
        self._mailedBy = mailed_by
        self._signedBy = signed_by
        self._content = content #code of the content 
        self._to = usercode
        self._code = hashcode
        
class Content:
    TEXT = "text"
    ATTACHMENTS = "attachments"
    MESSAGE_CODE = "messageCode"
    CODE = "code"    
    def __init__(self,message_code,hashcode=None, text=None,attachments=None ):
        self._code = hashcode
        self._messageCode = message_code
        self._text = text 
        self._attachments = attachments
        
class CDRFile:
    FILE_ID = "file_id"
    NAME = "name"
    CODE = "code"
    SIZE = "size"
    CONTENT_CODE = "contentCode"
    TYPE = "type"
    def __init__(self, hashcode, file_name  , content_code ,system_path = None,file_id=None):
        self._FileID = file_id
        self._Name = file_name
        self._code = hashcode
        self._size = os.path.getsize(system_path)
        self._contentCode = content_code
        self._LocalPath = system_path
        self._type = os.path.splitext(system_path)[-1]
        

class Logs:
    FILE_ID = "File_ID"
    LOGS = "logs"
    CODE = "code"
    def __init__(self,file_id,hashcode=None,logs = None):
        self._FileID = file_id
        self._logs = logs #List of logs
        self._code = hashcode
