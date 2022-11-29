from cdr import EmailProcess
from Email.utils.receiver import EmailReceiver
from Email.models.user import user
from Components.SpamProcessor import Analyze_Message
import os

IMAP_SERVERS ={
    "gmail":"imap.gmail.com",
    "yahoo":"imap.mail.yahoo.com",
    "yahoo.plus":"plus.imap.mail.yahoo.com",
    "yahoo.uk":"imap.mail.yahoo.co.uk",
    "yahoo.au":"imap.mail.yahoo.au",
    "aol":"imap.aol.com",
    "att":"imap.att.yahoo.com",
    "ntl":"imap.ntlworld.com",
    "btconnect":"imap4.btconnect.com",
    "outlook":"imap-mail.outlook.com"
}

def getEmails(email : str,appkey : str):
    
    
    def extract_domain(email_address : str): 
        """extract the IMAP server from email address
        
        Keyword arguments:
        email -- user email address
        Return: A server domain (if exists else None)
        """        
        domain = email_address.split('@')[-1] #type(domain) is str
        if domain in IMAP_SERVERS:
            return IMAP_SERVERS[domain]
        splitter = domain.split('.') #type(splitter) is List[str]
        if len(splitter) == 0 :
            return None
        idx = -1
        domain_test = splitter[idx + 1]
        while  idx+1 < len(splitter) - 1:
            if domain_test in IMAP_SERVERS:
                return IMAP_SERVERS[domain_test]
            idx +=1
            if idx >= len(splitter) :
                return None 
            domain_test = domain_test +'.'+ splitter[idx + 1]
        return None
    
    
    server_domain = extract_domain(email_address= email)
    User = user(email,appkey,server_domain)
    Emailreceiver = EmailReceiver(User,'Inbox')
    emails ,count = Emailreceiver.receiver(1)
    clone = emails
    for msg in clone:
        # check if the email message is a spam
        if Analyze_Message(msg["content"]):
            emails.pop(msg)
            continue
        
        process = EmailProcess(files = msg["files"])
        process.CDR()
    
    for msg in emails:
        for filepath in msg["files"]:
            if not os.path.isfile(filepath):
                emails[msg]["files"].remove(filepath)        
    
    return emails,count
        
                     
    
