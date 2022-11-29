import os
import sys
sys.path.append(os.path.abspath('C:\\temp\\NAC\\FinalProject\\CDRFP\\CDRFinal\\Server\\flaskServer\\'))#Database path

import user.Database.database as DB
from user.Database.Entities import User 
CDR_PATH = "..//CDR_ROOM"

# from message import Message
class user:
    
    def __init__(self,email_address,appkey,imapserver):
        doc = DB.DataBase()._users.find_one({User.EMAIL_ADDRESS: email_address})
        if doc is None:
            DB.DataBase().insert_user(email_address,appkey)
        doc = DB.DataBase()._users.find_one({User.EMAIL_ADDRESS: email_address})
        DirPath =CDR_PATH+'//'+doc[User.CODE]
        if not os.path.isdir(DirPath):           
            os.mkdir(DirPath)
        self._dir = DirPath
        self._credentials = [email_address,appkey,imapserver]

    def getMessages(self):
        pass
        
          