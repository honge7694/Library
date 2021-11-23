from flask import Blueprint, render_template, request, url_for, session, redirect, flash
from models.library import library
from models.rental import libraryRental, db
from models.reply import libraryReply

bp = Blueprint('rentalrecord', __name__, url_prefix='/record')

@bp.route('/')
def record_home():
    if 'user' not in session:
        flash("권한이 없습니다.")
        return redirect(url_for('main.home'))
    
    user_email = session['user']

    # 페이지
    page = request.args.get('page', type=int, default=1)

    # 책 정보를 가져오기 위하여 join
    library_rental_list = db.session.query(library.idx, library.name, libraryRental.idx.label('rental_idx'), libraryRental.user_email, libraryRental.rental_date, libraryRental.return_date).filter(libraryRental.book_idx == library.idx, libraryRental.return_date != None, libraryRental.user_email == user_email).order_by(libraryRental.rental_date)

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

    return render_template('rental_record.html', rental_list=rental_list, avg=avg)