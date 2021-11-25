from flask import Blueprint, render_template, request, url_for, session, redirect, flash
from models.users import *
from werkzeug.security import generate_password_hash, check_password_hash
import re

bp = Blueprint('register', __name__, url_prefix='/register')

# 이메일 유효성 검사.
def send_mail(email):
    if not re.match('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
        return False
    return True

# 비밀번호 유효성 검사.
def send_password(password):
    
    # 숫자 + 알파벳.
    if re.findall('[0-9]+', password) and  \
        re.findall('[a-z]', password) or re.findall('[A-Z]', password):
        return True

    # 숫자 + 특문
    elif re.findall('[0-9]+', password) and re.findall('[`~!@#$%^&*(),<.>/?]+', password):
        return True
    
    # 알파벳 + 특문
    elif re.findall('[a-z]', password) or re.findall('[A-Z]', password) and re.findall('[`~!@#$%^&*(),<.>/?]+', password):
        return True
    
    # 알파벳 + 숫자 + 특문
    elif re.findall('[0-9]+', password) and re.findall('[a-z]', password) or re.findall('[A-Z]', password) and re.findall('[`~!@#$%^&*(),<.>/?]+', password):
        return True

    return False

# 이름 유효성 검사.
def send_name(name):
    if re.findall('[a-z]', name) or re.findall('[A-Z]', name):
        return True
    elif re.compile('[^ \u3131-\u3163\uac00-\ud7a3]+'):
        return True

    return False
@bp.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':

        # register.html에서 입력한 form 데이터 받기.
        user_email = request.form['user_email']
        user_pw = request.form['user_pw']
        user_name = request.form['user_name']

        # 만들어진 email이 존재하는지 검사
        user = User.query.filter_by(email=user_email).first()

        # email이 존재하지 않는다면.
        if not user:
            if len(user_pw) < 7:
                flash("비밀번호 길이는 8자리 이상입니다.")
                return redirect(url_for('register.register'))
            
            # 1차 비번과 2차비번이 같지 않다.
            if user_pw != request.form['user_pw2']:
                flash("비밀번호가 같지않습니다.")
                return redirect(url_for('register.register'))

            # 이메일 형식 검사
            if send_mail(user_email) == False:
                flash('이메일을 형식에 맞게 입력해주세요.')
                return redirect(url_for('register.register'))

            # 비밀번호 유효성 검사
            if send_password(user_pw) == False:
                flash('영문, 숫자, 특수문자 중 2가지 이상을 혼합하여 입력해주세요.')
                return redirect(url_for('register.register'))

            # 이름 유효성 검사
            if send_name(user_name) == False:
                flash('이름은 한글 및 영어로만 입력해주세요.')
                return redirect(url_for('register.register'))

            # 비밀번호를 hash형태로 저장.
            password = generate_password_hash(request.form['user_pw'])

            # 유저 추가
            user = User(user_email, password, user_name)
            
            db.session.add(user)
            db.session.commit()

            flash('회원가입을 완료했습니다.')
            return redirect(url_for('login.login'))
        else:
            flash("이미 존재하는 이메일 입니다.")
            # 사용자가 있으면 register redirect
            return redirect(url_for('register.register'))

    