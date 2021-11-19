from flask import Blueprint, render_template, request, url_for, session, redirect, flash
from models import *
from models.library import libraryRental
import os

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/', methods=('GET', 'POST'))
def home():
    if request.method == 'GET':
        library = libraryRental.query.order_by(libraryRental.idx).all()

        # 실험 S
        files=[]
        for book in library:
            if (os.path.isfile('/static/book_img/{}.png'.format(book.idx))):
                files.append(os.path.isfile('/static/book_img/{}.png'.format(book.idx)))
            else:
                files.append(os.path.isfile('/static/book_img/{}.jpg'.format(book.idx)))
            print(book.idx, " : ", files[book.idx-1])
        # 실험 E
        return render_template('main_view.html', books=library, file=files)
    else:
        # library 대여하기 클릭.
        None