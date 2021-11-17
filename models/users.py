from db_connect import db


class User(db.Model):

    __tablename__ = 'libraryUser'

    email        = db.Column(db.String(255), primary_key=True,nullable=False)
    password     = db.Column(db.String(255), nullable=False)
    name         = db.Column(db.String(30), nullable=False)

    def __init__(self, email, password, name):
            self.email = email
            self.password = password
            self.name = name



