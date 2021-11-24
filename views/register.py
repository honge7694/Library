from flask import Blueprint, render_template, request, url_for, session, redirect, flash
from models.users import *
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('register', __name__, url_prefix='/register')

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

        # TODO 선택 기능 수행 / 이름 영어 한글 / 이메일은 이메일로만
        # email이 존재하지 않는다면.
        if not user:
            if len(user_pw) < 7:
                flash("비밀번호 길이는 8자리 이상입니다.")
                return redirect(url_for('register.register'))
            
            # 1차 비번과 2차비번이 같지 않다.
            if user_pw != request.form['user_pw2']:
                flash("비밀번호가 같지않습니다.")
                return redirect(url_for('register.register'))

            # 비밀번호를 hash형태로 저장.
            password = generate_password_hash(request.form['user_pw'])

            # 유저 추가
            user = User(user_email, password, user_name)
            
            db.session.add(user)
            db.session.commit()

            return redirect(url_for('login.login'))
        else:
            flash("이미 존재하는 이메일 입니다.")
            # 사용자가 있으면 register redirect
            return redirect(url_for('register.register'))

    