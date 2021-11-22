from db_connect import db

class libraryReply(db.Model):

    __tablename__ = 'libraryReply'

    idx          = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    book_idx = db.Column(db.Integer, db.ForeignKey('libraryBook.idx'), nullable=False)
    user_email = db.Column(db.String(255), db.ForeignKey('libraryUser.email'), nullable=False)
    contents = db.Column(db.Text(), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    write_date = db.Column(db.String(30), nullable=False)
    
    def __init__(self, book_idx, user_email, contents, rating, write_date):
        self.book_idx = book_idx
        self.user_email = user_email
        self.contents = contents
        self.rating = rating
        self.write_date = write_date