from flask import Blueprint, render_template, request, url_for, session, redirect, flash
from models.library import library
from models.reply import libraryReply
from models.rental import libraryRental, db
from datetime import datetime
from pytz import timezone

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/', methods=['GET'])
def home():
    
    if request.method == 'GET':
        # 페이지
        page = request.args.get('page', type=int, default=1)
        library_list_all = library.query.order_by(library.idx)
        #페이지 개수 표시 per_pate : 12개
        library_list = library_list_all.paginate(page, per_page=12)

        reply_ratings = libraryReply.query.filter(libraryReply.book_idx == library.idx).all()
        
        # 별점 계산
        total_sum, count, avg = 0, 0, []
        for book in library_list_all:
            for reply in reply_ratings:
                if(book.idx == reply.book_idx):
                    total_sum += reply.rating
                    count += 1
            if(total_sum != 0):
                avg.append(int(total_sum / count))
                total_sum, count = 0, 0
            # 배열이기 때문에 순차적으로 평균을 나타내준다.
            else:
                avg.append(0)

        return render_template('main_view.html', books=library_list, avg=avg)

@bp.route('/rental/<int:book_idx>')
def book_rental(book_idx):
    if 'user' not in session:
        flash('권한이 없습니다.')
        return redirect(url_for('main.home'))
    user_email = session['user']
    book_index = book_idx

    # 책 개수 확인.
    librarybook = library.query.filter(library.idx == book_index).first()

    # 빌린 책인지 확인.
    rental_book = libraryRental.query.filter(libraryRental.user_email == user_email).all()
    for rental in rental_book:
        if rental.user_email == user_email and rental.book_idx == book_index:
            if rental.return_date == None:
                flash('이미 대여 중인 책입니다.')
                return redirect(url_for('main.home'))

    if librarybook.count == 0:
        flash('대여가능한 책이 없습니다.')
        return redirect(url_for('main.home'))
        
    rental_date = datetime.now(timezone('Asia/Seoul')).strftime("%Y-%m-%d %H:%M:%S")
    rental = libraryRental(book_idx, user_email, rental_date)

    db.session.add(rental)
    db.session.commit()
    
    librarybook.count -= 1

    db.session.add(librarybook)
    db.session.commit()
    
    flash('책을 대여했습니다.')
    return redirect(url_for('main.home', page=pageNum))

