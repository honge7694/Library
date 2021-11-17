from flask import render_template, Blueprint, request, url_for, session, redirect, flash
from models.users import *
from werkzeug.security import check_password_hash

bp = Blueprint('login', '__name__', url_prefix='/login')

bp.route('/', methods=['GET', 'POST'])
def login():
    
    if request.method == 'GET':
        return render_template('login.html')
    
    elif request.method == 'POST':
        user_email = request.form['user_email']
        user_pw = request.form['user_pw']

        user = User.request.filter(User.email == user_email).first()

        if not user:
            flash('이메일을 확인해주세요.')
            return redirect(url_for('login.login'))
        elif not check_password_hash(user.password, user_pw):
            flash('비밀번호를 확인해주세요.')
            return redirect(url_for('login.login'))
        else:
            session.clear()
            session['user'] = user_email
            session['name'] = user.name

            return redirect(url_for('main.home'))

        
