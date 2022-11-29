import imaplib
import email
# import user.Database.database as DBAccess
# import user.Database.Entities as model
# from models.user import user
import os
import os
import sys
sys.path.append(os.path.abspath('C:\\Users\\user\\Desktop\\CDRFinal\\Server\\flaskServer\\user\\Email'))
import models.user as a

import hashlib

import base64

class EmailReceiver:
    
    def __init__(self,User : a.user ,keyword : str):
        """_summary_

        Args:
            email_address (str): email address
            AppKey (str): password from kareem(server-side)
            keyword (str): the type of emails(inbox,spam,etc.)
        """
        self._email = User._credentials[0]
        self._password = User._credentials[1]
        self._imapserver = User._credentials[2]
        self._option = keyword
        self._dir = User._dir
    
    def receiver(self,number):
        AttahcmentsPath = None
        dict = {} 
        count  = 0       
        imap = imaplib.IMAP4_SSL(self._imapserver)
        imap.login(self._email,self._password)
        imap.select(self._option)
        _,arr = imap.search(None,'ALL')
        for message in arr[0].split():
            if count==number:
                break
            count += 1
            filelists = [] 
            _,data = imap.fetch(message,"(RFC822)")        
            raw_email = data[0][1]
            raw_email_string = raw_email.decode('utf-8')
            email_message = email.message_from_string(raw_email_string)
            del raw_email,raw_email_string
            From = email_message.get('From')
            to = email_message.get('To')
            bcc = email_message.get('BCC')
            date = email_message.get('Date')
            subject = email_message.get('Subject')
            subdict = {}
            temp=From+date
            subdict['mailCode']=hashlib.sha256(temp.encode()).hexdigest()
            subdict["from"]=From
            subdict["to"] = to
            subdict["bcc"] = bcc
            subdict["subject"] = subject
            subdict["date"] = date
            firstTime = True
            content = ''    
            # iterate through the tree of mail
            for part in email_message.walk():
                
                if part.get_content_type() == 'text/plain':
                    def isBase64(sb):
                        import re
                        return len(sb) % 4 == 0 and re.search('^[A-Za-z0-9+/]+[=]{0,3}$',sb)
                    if not isBase64(part.get_payload()):
                        content += part.get_payload()
                        
                    continue
                if part.get_content_type() == 'multipart':
                    continue
                if part.get('Content-Disposition') is None:
                    continue
                filename = part.get_filename()
                if firstTime :
                    firstTime = False
                    AttahcmentsPath = self._dir + '//' + str(count)
                    if not os.path.isdir(AttahcmentsPath):
                        os.mkdir(AttahcmentsPath)            
                if bool(filename):
                    filepath = AttahcmentsPath+'//'+filename
                    
                    if not os.path.isfile(filepath):
                        fd = open(filepath,'wb')
                        fd.write(part.get_payload(decode=True))
                        fd.close()
                        filelists.append(filepath[4:])
            if filelists is not []:
                subdict["files"] = filelists
                subdict["content"] = content
                dict[count] = subdict
        
        return dict , count
                    
         
