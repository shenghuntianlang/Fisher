"""
The database model to show relationship between user and book
"""
from flask import current_app
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, desc, func
from sqlalchemy.orm import relationship

from app.models.base import Base, db
from app.spider.yushu_book import YuShuBook


class Gift(Base):
    id = Column(Integer, primary_key=True)
    # 声明表关系
    user = relationship('User')
    # ForeignKey: 外联
    uid = Column(Integer, ForeignKey('user.id'))

    isbn = Column(String(15), nullable=False)
    # 书籍是否被送出,默认为false
    launched = Column(Boolean, default=False)

    def is_yourself_gift(self, uid):
        return True if self.uid == uid else False

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first

    @classmethod
    def get_user_gifts(cls, uid):
        gifts = Gift.query.filter_by(uid=uid, launched=False).order_by(
            desc(Gift.create_time)).all()
        return gifts

    @classmethod
    def get_wish_counts(cls, isbn_list):
        # 根据传入的一组isbn编号,到Gift表中检索相应的礼物,并计算出某个礼物
        # 的Wish心愿数量
        # filter中传入的是表达式而不是关键词参数
        from app.models.wish import Wish
        count_list = db.session.query(func.count(Wish.id), Wish.isbn).filter(
            Wish.launched == False,
            Wish.isbn.in_(isbn_list),
            Wish.status == 1).group_by(
            Wish.isbn).all()
        return [{'count': w[0], 'isbn': w[1]} for w in count_list]

    # 对象代表一个礼物,具体
    # 类代表这个事物,它是抽象的,不是具体的"一个"
    @classmethod
    def recent(cls):
        recent_gift = Gift.query.filter_by(
            launched=False).group_by(  # 分组,为distinct去重创造条件
            Gift.isbn).order_by(  # 排序,以便limit正确截取指定数量的结果集
            desc(Gift.create_time)).limit(
            current_app.config['RECENT_GIFT_COUNT']).distinct().all()
        return recent_gift
