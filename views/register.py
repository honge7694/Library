from flask import Blueprint, render_template, request, url_for, session, redirect, flash
from models.users import *
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('register', __name__, url_prefix='/register')

@bp.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        user = User.query.filter(User.email == request.form['user_email']).first()

        # email이 존재하지 않는다면.
        if not user:
            if len(request.form['user_pw']) < 7:
                flash("비밀번호 길이는 8자리 이상입니다.")
                return redirect(url_for('register.register'))
            password = generate_password_hash(request.form['user_pw'])

            # 유저 추가
            user = User(request.form['user_email'], password, request.form['user_name'])
            
            db.session.add()
            db.session.commit()

            return render_template(url_for('login.login'))
        else:
            return redirect(url_for('register.register'))

    