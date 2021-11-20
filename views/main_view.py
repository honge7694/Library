from flask import Blueprint, render_template, request, url_for, session, redirect, flash
from models import *
from models.library import libraryRental
import os

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/', methods=('GET', 'POST'))
def home():
    if request.method == 'GET':
        # 페이지
        page = request.args.get('page', type=int, default=1)
        library_list = libraryRental.query.order_by(libraryRental.idx)
        library_list = library_list.paginate(page, per_page=10)

        
        return render_template('main_view.html', books=library_list)
    else:
        # library 대여하기 클릭.
        None