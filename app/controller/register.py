from app.models import *
from app import db,app
from dotenv import load_dotenv
from flask_mail import Mail,Message
import os
from random import randint
from itsdangerous import URLSafeTimedSerializer

load_dotenv(dotenv_path='./env/email.env')
MAIL_SERVER = os.getenv('MAIL_SERVER')
MAIL_PORT = os.getenv('MAIL_PORT')
MAIL_USERNAME = os.getenv('MAIL_USERNAME')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
SECRET_KEY = os.getenv('SECRET_KEY')

app.config["MAIL_SERVER"]=MAIL_SERVER
app.config["MAIL_PORT"]=MAIL_PORT
app.config["MAIL_USERNAME"]=MAIL_USERNAME
app.config['MAIL_PASSWORD']=MAIL_PASSWORD
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True
app.config['SECRET_KEY']=SECRET_KEY
app.config['SECURITY_PASSWORD_SALT']='email-confirm'
mail=Mail(app)


def generate_confirmation_token(email):
    otp=str(randint(100000,999999))
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=otp), otp

def confirm_token(token,opt, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=opt,
            max_age=expiration
        )
    except:
        return False
    return email

def send_email(to, otp):
    msg = Message('Confirm Email OTP', sender=app.config["MAIL_USERNAME"], recipients=[to])
    msg.body= 'OTP : '+ str(otp)
    mail.send(msg)

def check_user_name(username):
    user = db.session.query(User).filter(User.username.like(username)).first()
    if (user):
        return 1
    else:
        return 0

def check_email(email):
    user = db.session.query(User).filter(User.email.like(email)).first()
    if (user):
        return 1
    else:
        return 0

def check_input_register(username, password, retypepassword, fullname, email):
    # check username
    if username == None or username == '':
        return "Nhap username"
    for c in username:
        if (ord(c) >= 97 and ord(c) <= 119) or (ord(c) >= 48 and ord(c) <= 57) or (ord(c) >= 65 and ord(c) <= 87):
            continue
        return "username khong duoc co ky tu dac biet"
        

    # check pass
    if password == None or password == '':
        return "Nhap mat khau"
    if len(password) < 8 :
        return "Mat khau phai tren 8 ky tu"
    if password != retypepassword:
        return "Mat khau khac nhau, nhap lai"

    # check full name
    if fullname == None or fullname == '':
        return "Nhap ten"
    for c in fullname:
        if (ord(c) >= 97 and ord(c) <= 119) or (ord(c) >= 48 and ord(c) <= 57) or (ord(c) >= 65 and ord(c) <= 87) or (c == ' '):
            continue
        return "Ten khong duoc co ky tu dac biet"

    # check email
    cntA = 0
    cntD = 0
    for c in email:
        if c == '@':
            cntA = cntA + 1
        if c == '.':
            cntD = cntD + 1
    if cntA != 1 or cntD != 1:
        return "Nhap sai email"

    return True

def get_all_type_account():
    all_type_account = TypeAccount.query.all()
    return all_type_account

def insert_new_user(type_account_id, username, passwd, fullname, email, birthday=None, highest_degree=None, university=None, major=None):
    typeAccount = db.session.query(TypeAccount).filter(TypeAccount.type_name.like('Student')).first()
    user = User(username, passwd, fullname, email)
    typeAccount.users.append(user)

    db.session.add(user)
    db.session.commit()
