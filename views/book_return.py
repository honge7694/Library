from flask import Blueprint, render_template, request, url_for, session, redirect, flash
from models.library import library
from models.rental import libraryRental, db
from models.reply import libraryReply
from datetime import datetime
from pytz import timezone

bp = Blueprint('bookreturn', __name__, url_prefix='/return')

@bp.route('/')
def return_home():
    if 'user' not in session:
        flash("권한이 없습니다.")
        return redirect(url_for('main.home'))
    
    user_email = session.get('user')

    # 페이지
    page = request.args.get('page', type=int, default=1)

    # 책 정보를 가져오기 위하여 join
    library_rental_list = db.session.query(library.idx, library.name, libraryRental.idx.label('rental_idx'), libraryRental.user_email, libraryRental.rental_date).filter(libraryRental.book_idx == library.idx, libraryRental.return_date == None, libraryRental.user_email == user_email).order_by(libraryRental.rental_date)

    # 페이지 개수 표시 per_pate : 12개
    rental_list = library_rental_list.paginate(page, per_page=12)
    reply_ratings = libraryReply.query.filter(libraryReply.book_idx == libraryRental.book_idx).all()
    
    # 별점 계산
    total_sum, count, avg = 0, 0, []
    for book in library_rental_list:
        for reply in reply_ratings:
            if(book.idx == reply.book_idx):
                total_sum += reply.rating
                count += 1
        if(total_sum != 0):
            avg.append(int(total_sum / count))
            total_sum, count = 0, 0

    return render_template('book_return.html', rental_list=rental_list, avg=avg)

@bp.route('/return_book/<int:book_idx>')
def book_return(book_idx):
    # rental_idx를 받아온다.
    rental_index = request.args.get('rental_idx')

    book_index = book_idx
    # 반납시간
    today = datetime.now(timezone('Asia/Seoul')).strftime("%Y-%m-%d %H:%M:%S")    

    # 반납
    rental = libraryRental.query.filter(libraryRental.book_idx == book_index, libraryRental.idx == rental_index).first()
    rental.return_date = today

    db.session.add(rental)
    db.session.commit()

    # 재고 증가
    book = library.query.filter(library.idx == book_idx).first()
    book.count += 1

    db.session.add(book)
    db.session.commit()

    flash('반납이 완료되었습니다.')
    return redirect(url_for('bookreturn.return_home'))