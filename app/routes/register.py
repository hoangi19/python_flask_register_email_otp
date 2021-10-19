from app import app
from app.controller import *
from flask import render_template, request, flash, redirect, url_for
import json

@app.route('/register.html', endpoint='render_register')
def render_register():
    return render_template('register.html')

@app.route('/otp_vertify.html', endpoint='render_otp_vertify')
def render_otp_vertify():
    messages=request.args['messages']
    print(messages)
    return render_template('otp_vertify.html', messages=json.loads(messages))
@app.route('/otp_vertify', endpoint='opt_vertify', methods=['POST'])
def otp_vertify():
    _otp = request.form.get('otp')
    _token = request.form.get('token')
    # print(_opt)
    # print(_token)
    data = confirm_token(_token, _otp)
    if data == False:
        flash(False)
        return redirect(url_for('render_otp_vertify', messages=json.dumps({"token": _token})))
    data = json.loads(data)
    insert_new_user('student', data['username'], data['password'], data['full_name'], data['email'])
    flash('Register_Success')
    return redirect('login.html')

@app.route('/register', endpoint='register', methods=['POST'])
def register():
    _username = request.form.get('username')
    _passwd = request.form.get('password')
    _retype_passwd = request.form.get('retypepassword')
    _full_name = request.form.get('fullname')
    _email = request.form.get('email')
    _birthday = request.form.get('birthday')
    _type_account = 'student'
    _highest_degree = request.form.get('highest_degree')
    _university = request.form.get('university')
    _major = request.form.get('major')

    status = check_input_register(_username, _passwd, _retype_passwd, _full_name, _email)

    if(status == True):
        if (check_user_name(_username)):
            flash("username already exist")
            return redirect('/register.html')
        elif (check_email(_email)):
            flash("email already exist")
            return redirect('/register.html')
        else:
            data = json.dumps({
                "email" : _email,
                "username" : _username,
                "password" : _passwd,
                "full_name" : _full_name,
                })
            token, otp = generate_confirmation_token(data)
            send_email(_email, otp)
            flash("passed")
            return redirect(url_for('render_otp_vertify', messages=json.dumps({"token": token})))
    else:
        flash(status)
        return redirect('/register.html')