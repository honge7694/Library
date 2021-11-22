from flask import Blueprint, render_template, request, url_for, session, redirect, flash
from models.library import library
from models.reply import *
from datetime import datetime
from pytz import timezone


bp = Blueprint('detail', __name__, url_prefix='/detail')

@bp.route('/<int:book_idx>', methods=["GET"])
def book_detail(book_idx):

    if request.method == "GET":
        book = library.query.filter(library.idx == book_idx).first()
        reply = libraryReply.query.filter(libraryReply.book_idx == book_idx).order_by(libraryReply.idx.desc())

        return render_template('book_detail.html', book=book, reply_info=reply)

@bp.route('/write_reply/<int:book_idx>', methods=["POST"])
def create_reply(book_idx):
    if 'user' not in session:
        flash("권한이 없습니다.")
        return redirect(url_for('main.home'))

    user_email = session['user']
    reply_content = request.form['reply'] # html id 바꾸기.
    reply_rating = request.form['rating']

    # 날짜 
    today = datetime.now(timezone('Asia/Seoul')).strftime("%Y-%m-%d %H:%M:%S")    
    reply = libraryReply(book_idx, user_email, reply_content, reply_rating, today)
    
    db.session.add(reply)
    db.session.commit()

    flash("리뷰 작성 완료")
    return redirect(url_for('detail.book_detail', book_idx=book_idx))
