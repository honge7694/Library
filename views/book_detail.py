from flask import Blueprint, render_template, request, url_for, session, redirect, flash
from models import *
from models.library import libraryRental

bp = Blueprint('detail', __name__, url_prefix='/detail')

@bp.route('/<int:book_id>', methods=["GET"])
def book_detail(book_id):

    if request.method == "GET":
        book = libraryRental.query.filter(libraryRental.idx == book_id).first()

        return render_template('book_detail.html', book=book)