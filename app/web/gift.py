"""
the view functions about some operations for my gifts
"""

from flask import current_app, flash, redirect, url_for, render_template
from flask_login import login_required, current_user

from app.libs.enums import PendingStatus
from app.models.base import db
from app.models.drift import Drift
from app.models.gift import Gift
from app.view_models.trade import MyTrades
from . import web

__author__ = '七月'


@web.route('/my/gifts')
@login_required
def my_gifts():
    uid = current_user.id
    gifts_of_mine = Gift.get_user_gifts(uid)
    isbn_list = [gift.isbn for gift in gifts_of_mine]
    wish_count_list = Gift.get_wish_counts(isbn_list)
    view_model = MyTrades(gifts_of_mine, wish_count_list)
    return render_template('my_gifts.html', gifts=view_model.trades)


@web.route('/gifts/book/<isbn>')
@login_required
def save_to_gifts(isbn):
    if current_user.can_save_to_list(isbn):
        # 如果数据库操作时发生异常,则进行数据库回滚,否则会影响之后的数据库操作
        with db.auto_commit():
            gift = Gift()
            gift.isbn = isbn
            # current_user, 与current_app, request原理相同,用来获取当前登录的用户对象
            gift.uid = current_user.id
            # 每上传一本书获取一定数量的鱼豆
            current_user.beans += current_app.config['BEANS_UPLOAD_ONE_BOOK']
            db.session.add(gift)
    else:
        flash('该书已存在于您的赠送清单或愿望清单,请勿重复添加')
    return redirect(url_for('web.book_detail', isbn=isbn))


@web.route('/gifts/<gid>/redraw')
@login_required
def redraw_from_gifts(gid):
    gift = Gift.query.filter_by(id=gid, launched=False).first_or_404()
    if not gift:
        flash('该书籍不存在，或已经交易，删除失败')
    else:
        # filter_by中的条件关键词是数据库模型中的字段,而不是数据库中的字段
        drift = Drift.query.filter_by(gift_id=gid, _pending=PendingStatus.Waiting.value).first()
        if drift:
            flash('该礼物正在处于交易状态,请先前往鱼漂完成该交易')
        else:
            with db.auto_commit():
                current_user.beans -= current_app.config['BEANS_UPLOAD_ONE_BOOK']
                gift.delete()

    return redirect(url_for('web.my_gifts'))
