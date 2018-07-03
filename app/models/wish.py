"""
The database model to show relationship between user and book
"""
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, desc, func
from sqlalchemy.orm import relationship

from app.models.base import Base, db
from app.spider.yushu_book import YuShuBook


class Wish(Base):
    id = Column(Integer, primary_key=True)
    # 声明表关系
    user = relationship('User')
    # ForeignKey: 外联
    uid = Column(Integer, ForeignKey('user.id'))

    isbn = Column(String(15), nullable=False)
    # 书籍是否被送出,默认为false
    launched = Column(Boolean, default=False)

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first

    @classmethod
    def get_user_wishes(cls, uid):
        wishes = Wish.query.filter_by(uid=uid, launched=False).order_by(
            desc(Wish.create_time)).all()
        return wishes

    @classmethod
    def get_gift_counts(cls, isbn_list):
        # 根据传入的一组isbn编号,到Gift表中检索相应的礼物,并计算出某个礼物
        # 的Wish心愿数量
        # filter中传入的是表达式而不是关键词参数
        from app.models.gift import Gift
        count_list = db.session.query(func.count(Gift.id), Gift.isbn).filter(
            Gift.launched == False,
            Gift.isbn.in_(isbn_list),
            Gift.status == 1).group_by(
            Gift.isbn).all()
        return [{'count': w[0], 'isbn': w[1]} for w in count_list]
