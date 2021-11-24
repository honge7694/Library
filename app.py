from flask import Flask, render_template
from db_connect import db
from flask_migrate import Migrate
import config
from views import main_view, register, login, book_detail, book_return, rental_record


#Flask 객체 인스턴스 생성
def create_app():

    app = Flask(__name__)

    # db 연결
    app.config.from_object(config) # config에서 가져온 파일을 사용한다.
    #app.secret_key = "seeeeeeeeeeeeeecret"
    app.config['SESSION_TYPE'] = 'filesystem'

    db.init_app(app) # SQLAlchemy 객체를 app 객체와 이어준다.
    Migrate().init_app(app, db)

    # view Blueprint 등록
    app.register_blueprint(main_view.bp)
    app.register_blueprint(register.bp)
    app.register_blueprint(login.bp)
    app.register_blueprint(book_detail.bp)
    app.register_blueprint(book_return.bp)
    app.register_blueprint(rental_record.bp)
    return app

if __name__=="__main__":
  create_app().run(debug=True)