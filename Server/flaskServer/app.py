
from flask import Flask,render_template ,session ,redirect,request , send_file

from functools import wraps
from user.Database import database
from user.Email.models import *
from user.Email.utils.receiver import *
from user.Email.models import user as SessionUser
from flask_caching import Cache

app = Flask(__name__)
DB=database.DataBase()
app.secret_key='temporary_secret'
cache=Cache()
app.config['CACHE_TYPE']='simple'

cache.init_app(app)

def login_required(func):
    @wraps(func)
    def wrap(*arg,**Kwargs):
        if 'logged_in' in session:
            return func(*arg,**Kwargs)
        else :
            return redirect('/') #later should be redirected a 405 error 
    return wrap


from user import routes

mails=None

@app.route('/Home/', methods=['GET','POST'])
@login_required
#@cache.cached(timeout=10, key_prefix='homeMails')
def Home():



    CurrentUser=SessionUser.user(session.get('user')['email'],session.get('user')['password'],'imap.gmail.com')
    
    
    Reciver=EmailReceiver(CurrentUser,'Inbox')
    global mails

    if request.method=="GET":
        arr=Reciver.receiver(5)
        mails=arr[0]

        FROM_SUBJECT={}
        HAshCode={}

        for i in range(arr[1]):
            print(mails[i+1]['from'])
            FROM_SUBJECT[mails[i+1]['mailCode']]=(mails[i+1]['from'],mails[i+1]['subject'])
            print(FROM_SUBJECT)
            

        
        return render_template('Home.html',UserEmails=FROM_SUBJECT ,Loggedin=1 ,mail=mails)

    if request.method=='POST':
        
        ClickedMailCode=request.form['custId']
        Number=0
        for key in mails:
            print('------------------------------------------')
            print(mails[key])
            print('------------------------------------------')

            if mails[key]['mailCode']==ClickedMailCode:
                Number=key

        From=mails[Number]['from']
        to=mails[Number]["to"] 
        bcc=mails[Number]['bcc']
        subject=mails[Number]['subject']
        date=str(mails[Number]['date'])
        fileslists=mails[Number]['files']
        content=mails[Number]['content']

                            
        
        return render_template('Mail.html',From=From,to=to,bcc=bcc,subject=subject,date=date,fileslists=fileslists,content=content)
        



@app.route('/instructions')
def instruct():
    return render_template('ins.html')

@app.route('/download' , methods=['post'])
def download():
    
    path=request.form['path']
    return send_file(path,as_attachment=True)

@app.route('/')
def register():
    if 'logged_in' in session:
        return redirect('/Home/')
    else:
        return render_template('signup.html')
    


if __name__ == '__main__':

	app.run()
