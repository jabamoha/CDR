from flask import Flask , jsonify , request ,session,redirect
import uuid
from passlib.hash import pbkdf2_sha256
from user.Database import database
from user.Email.utils.authentication import *
from user.Email.utils.receiver import *
from user.Email.models import user as SessionUser

DB=database.DataBase()


class User:

    def start_session(self,user):
        session['logged_in']=True

        session['user']=user
        session['Mail']=None

        return jsonify(user),200

    
    def signup(self):
        user={
            "_id":uuid.uuid4().hex,
            "email":request.form.get('email'),
            "password":request.form.get('passphrase')
        }

        
        DB.insert_user(user['email'],user['password']) 

        status=vaild_credentials(user['email'],user['password'])


        
        if status==False:

            return jsonify({"error":"Wrong Credintials"}) ,400
            

        if status==True:
            print('every thing is fine')
            return self.start_session(user)   
    def signout(self):
        session.clear()
        return redirect('/')

