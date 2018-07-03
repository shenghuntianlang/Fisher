"""
the view functions about operations for books
"""

# 在请求路由后面通过包裹'<>'的形式表示需要传入的参数,
# 视图参数会自动获取到其中的参数

from flask import request, render_template, flash
from flask_login import current_user

from app.forms.book import Searchform
from app.libs.helper import is_isbn_or_key
from app.models.gift import Gift
from app.models.wish import Wish
from app.spider.yushu_book import YuShuBook
from app.view_models.book import BookCollection, BookViewModel
from app.view_models.trade import TradeInfo
from app.web import web


# 通过蓝图注册路由,然后再由app对象注册蓝图,
# 达到视图函数分离的目的
# @web.route('/book/search/<q>/<page>')
@web.route('/book/search')
def search():
    # 验证层
    form = Searchform(request.args)

    books = None
    if form.validate():
        # 使用q的strip函数去除首尾空格,提高用户体验
        books = __is_form_accorded(q=form.q.data.strip(), page=form.page.data)
    else:
        flash('搜索关键字不符合要求,请重新输入')

    return render_template('search_result.html', books=books)


@web.route('/book/<isbn>/detail')
def book_detail(isbn):
    # 去书籍详情数据
    yushu_book = YuShuBook()
    yushu_book.search_by_isbn(isbn)
    book = BookViewModel(yushu_book.first)

    has_in_wishes, has_in_gifts = __confirm_book_state(isbn)

    trade_gifts = TradeInfo(Gift.query.filter_by(isbn=isbn, launched=False).all())
    trade_wishes = TradeInfo(Wish.query.filter_by(isbn=isbn, launched=False).all())

    return render_template('book_detail.html', book=book, wishes=trade_wishes, gifts=trade_gifts,
                           has_in_wishes=has_in_wishes, has_in_gifts=has_in_gifts)


def __confirm_book_state(isbn):
    """
    确定书籍的状态,是否在当前用户的心愿表或赠送表中
    :param isbn:
    :return:
    """
    has_in_wishes = False
    has_in_gifts = False
    if current_user.is_authenticated:
        if Wish.query.filter_by(uid=current_user.id, isbn=isbn, launched=False).first():
            has_in_wishes = True
        if Gift.query.filter_by(uid=current_user.id, isbn=isbn, launched=False).first():
            has_in_gifts = True
    return has_in_wishes, has_in_gifts


def __is_form_accorded(q, page):
    """
    verify the request parameters' correctness
    :param q:
    :param page:
    :return:
    """
    # isbn13 13个0到9的数字组成
    # isbn10 10个0到9的数字组成,含有一些'-'
    isbn_or_key = is_isbn_or_key(q)
    books = BookCollection()
    yushu_book = YuShuBook()

    if 'isbn' == isbn_or_key:
        yushu_book.search_by_isbn(q)
    else:
        yushu_book.search_by_keyword(q, page)

    books.fill(yushu_book, q)
    # 返回的数据必须是字符串形式,而json格式的数据在Python中是dict形式
    # 因此,必须使用json的dumps函数对数据进行序列化
    # return json.dumps(books, default=lambda val: val.__dict__)
    # return json.dumps(result), 200, {'content-type': 'application/json'}
    return books
