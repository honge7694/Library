# 3기*도서관대출서비스*이름

## 11/16

- 프로젝트 생성
- app.py 파일 및 templates 폴더 생성
- ERD 설계

## 11/17

- db 생성 및 데이터 삽입
- 데이터 삽입에서 애를 먹었다..
- register, login 구현 (50%)
__코치님 피드백__
1. 유저인덱스를 사용보단 이메일로 사용.
2. 유저 이메일은 VARCHAR(255)로 규정되어 있다.
3. 가능하다면 책 테이블에서 물리적개념과 기능을 나눈다. ( 유연성 or 데이터 오염 가능성이 있다.)
4. 실제 서비스 db에서는 책 출판사와 저자를 나눈다.
5. 댓글테이블 comment로 변경
6. 댓글테이블 star는 integer로 사용.
7. 책설명과 댓글 내용은 text가 적절하다.

## 11/18

- login, register, 필수기능 구현완료
- main 카드리스트 및 데이터 불러오기.

