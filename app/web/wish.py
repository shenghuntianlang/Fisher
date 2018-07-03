"""
the view functions about some operations for my wishes
"""

from flask import flash, redirect, url_for, render_template
from flask_login import current_user, login_required

from app.libs.mail import send_mail
from app.models.base import db
from app.models.gift import Gift
from app.models.wish import Wish
from app.view_models.trade import MyTrades
from . import web

__author__ = '七月'


@web.route('/my/wish')
@login_required
def my_wish():
    uid = current_user.id
    wishes_of_mine = Wish.get_user_wishes(uid)
    isbn_list = [wish.isbn for wish in wishes_of_mine]
    gift_count_list = Wish.get_gift_counts(isbn_list)
    view_model = MyTrades(wishes_of_mine, gift_count_list)
    return render_template('my_wish.html', wishes=view_model.trades)


@web.route('/wish/book/<isbn>')
@login_required
def save_to_wish(isbn):
    if current_user.can_save_to_list(isbn):
        # 如果数据库操作时发生异常,则进行数据库回滚,否则会影响之后的数据库操作
        with db.auto_commit():
            wish = Wish()
            wish.isbn = isbn
            # current_user, 与current_app, request原理相同,用来获取当前登录的用户对象
            wish.uid = current_user.id
            db.session.add(wish)
    else:
        flash('该书已存在于您的赠送清单或愿望清单,请勿重复添加')
    return redirect(url_for('web.book_detail', isbn=isbn))


@web.route('/satisfy/wish/<int:wid>')
@login_required
def satisfy_wish(wid):
    wish = Wish.query.get_or_404(wid)
    gift = Gift.query.filter_by(uid=current_user.id, isbn=wish.isbn).first()
    if not gift:
        flash('你还没有上传此书,请点击"加入到赠送清单"添加此书.添加前,请确保自己可以赠送此书')
    else:
        send_mail(wish.user.email, '有人想赠送你一本书',
                  'email/satisify_wish.html', wish=wish, gift=gift)
        flash('已向他/她发送了一封邮件,如果/他/她愿意接受你的赠送,你将会收到一个鱼漂')
    return redirect(url_for('web.book_detail', isbn=wish.isbn))


@web.route('/wish/book/<isbn>/redraw')
@login_required
def redraw_from_wish(isbn):
    wish = Wish.query.filter_by(isbn=isbn, launched=False).first_or_404()
    with db.auto_commit():
        wish.delete()
    return redirect(url_for('web.my_wish'))
