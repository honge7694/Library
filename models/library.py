from db_connect import db

class library(db.Model):

    __tablename__ = 'libraryBook'

    idx          = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name    = db.Column(db.String(30))
    publisher = db.Column(db.String(30))
    author  = db.Column(db.String(30))
    publication_date = db.Column(db.String(50))
    page    = db.Column(db.Integer)
    isbn = db.Column(db.String(50))
    description   = db.Column(db.String(1000))
    count = db.Column(db.Integer)
    link   = db.Column(db.String(100))
    img_src = db.Column(db.String(50))
    

    #def __init__(self, book_name, publisher, author, publication_date, pages, isbn, description, link, img_src):
