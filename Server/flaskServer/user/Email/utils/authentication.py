import imaplib
from validate_email import validate_email

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

IMAP_PORT = 993

def validate(email_address):
    """validate if the email address is  really exists using SMTP and DNS

    Args:
        email_address (str): input email address

    Returns:
        bool: True if the email address is really exists ,else False
    """
    return validate_email(email_address)

@staticmethod
def vaild_credentials(email:str,password:str):
    """_summary_

    Args:
        email (str): user email
        password (str): user password

    Returns:
        bool : True,if the user credentials is correct else False
    """
    if not validate(email_address=email):
        return False
    
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
    
    server_domain = extract_domain(email_address = email)
    if server_domain is None:
        return False
    
    else:    
        imap = imaplib.IMAP4_SSL(server_domain)
        try:
            imap.login(email,password)
            ret = True
        except:
            ret = False
        return ret