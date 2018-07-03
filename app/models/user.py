"""
The database model for users
"""
from math import floor

from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy import Column, Integer, String, Boolean, Float
from werkzeug.security import generate_password_hash, check_password_hash

from app import login_manager
from app.libs.helper import is_isbn_or_key
from app.models.base import Base, db
from app.models.drift import Drift
from app.models.gift import Gift
from app.models.wish import Wish
from app.spider.yushu_book import YuShuBook


class User(UserMixin, Base):
    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    phone_number = Column(String(18), unique=True)
    email = Column(String(50), unique=True, nullable=False)
    _password = Column('password', String(255))
    confirmed = Column(Boolean, default=False)
    beans = Column(Float, default=0)
    send_counter = Column(Integer, default=0)
    receiver_counter = Column(Integer, default=0)
    wx_open_id = Column(String(50))
    wx_name = Column(String(32))

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    @property
    def summary(self):
        return dict(
            nickname=self.nickname,
            beans=self.beans,
            email=self.email,
            send_receive=str(self.send_counter) + "/" + str(self.receiver_counter)
        )

    def check_password(self, raw):
        return check_password_hash(self._password, raw)

    def can_save_to_list(self, isbn):
        if is_isbn_or_key(isbn) != 'isbn':
            return False
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(isbn)
        if not yushu_book.first:
            return False

        # 不允许同一用户同时赠送多本相同图书
        # 一个用户不可能同时成为赠送者和索要者
        gifting = Gift.query.filter_by(uid=self.id, isbn=isbn, launched=False).first()
        wishing = Wish.query.filter_by(uid=self.id, isbn=isbn, launched=False).first()
        # 如果礼物和愿望中都没有这本书,则允许用户将此礼物添加入礼物列表
        if not gifting and not wishing:
            return True
        else:
            return False

    def can_send_drift(self):
        # 如果鱼豆数量小于1,则不允许用户请求赠送书籍
        if self.beans < 1:
            return False
        # 成功送出的礼物数量
        success_gifts_count = Gift.query.filter_by(uid=self.id,
                                                   launched=True).count()
        # 成功接受到的赠书
        from app.libs.enums import PendingStatus
        success_receive_count = Drift.query.filter_by(requester_id=self.id,
                                                      pending=PendingStatus.Success).count()
        # 每接受两本赠书,就必须先赠出一本书之后才能继续接受赠书
        return True if floor(success_receive_count / 2) <= floor(success_gifts_count) else False

    def generate_token(self, expiration=600):
        # 实例化序列化器
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        # 写入用户信息信息,生成的是一串字节码,需要使用decode函数转码成一串字符串
        token = s.dumps({'id': self.id}).decode('utf-8')
        return token

    @staticmethod
    def reset_password(token, new_password):
        # 判空
        if not new_password:
            return False
        # 使用相同的SECRET_KEY实例化序列化器
        # 唯一字符串意义:如果别人拿不到这个唯一字符串,就几乎不可能拿到包含的内容
        s = Serializer(current_app.config['SECRET_KEY'])
        # 如果token非法或已过期,则序列化器会抛出异常,可以以此解决无效token的处理问题
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        # 使用键获取token中对应信息
        uid = data.get('id')
        # context_manager
        with db.auto_commit():
            # 如果查询条件体为数据表主键,则可以使用get方法直接查询
            user = User.query.get(uid)
            user.password = new_password
        return True

    # 如果User模型中代表用户id的column名不为id,则即使继承了UserMixin,也需要重写get_id方法.
    # def get_id(self):
    #     return self.id


@login_manager.user_loader
def get_user(uid):
    return User.query.get(int(uid))
