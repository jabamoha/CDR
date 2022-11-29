from flask import Flask,render_template
from app import app
from user.models import User



@app.route('/users/signup' , methods=['POST'])
def sign():
    user=User()

    return user.signup()
@app.route('/users/signout')
def signout():
    return User().signout()