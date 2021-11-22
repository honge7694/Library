from db_connect import db

class libraryRental(db.Model):

    __tablename__ = 'libraryRental'

    idx          = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    book_idx = db.Column(db.Integer, db.ForeignKey('libraryBook.idx'), nullable=False)
    user_email = db.Column(db.String(255), db.ForeignKey('libraryUser.email'), nullable=False)
    rental_date = db.Column(db.String(30), nullable=False)
    return_date = db.Column(db.String(30))

    def __init__(self, book_idx, user_email, rental_date):
        self.book_idx = book_idx
        self.user_email = user_email
        self.rental_date = rental_date