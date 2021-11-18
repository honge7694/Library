from flask import Blueprint, render_template, request, url_for, session, redirect, flash
from models import *
from models.library import libraryRental

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/', methods=('GET', 'POST'))
def home():
    if request.method == 'GET':
        library = libraryRental.query.all()

        return render_template('main_view.html', books=library)
    else:
        # library에서 책 가져오기.
        None