"""
the database model for drift
"""
from sqlalchemy import Column, Integer, String, SmallInteger

from app.libs.enums import PendingStatus
from app.models.base import Base


class Drift(Base):
    """
    一次交易的具体信息
    """
    id = Column(Integer, primary_key=True)

    # 邮寄信息
    recipient_name = Column(String(20), nullable=False)
    address = Column(String(100), nullable=False)
    message = Column(String(200))
    mobile = Column(String(20), nullable=False)

    # 书籍信息
    isbn = Column(String(13))
    book_title = Column(String(50))
    book_author = Column(String(30))
    book_img = Column(String(50))

    # 请求者信息
    requester_id = Column(Integer)
    requester_nickname = Column(String(20))

    # 赠送者信息
    gifter_id = Column(Integer)
    gift_id = Column(Integer)
    gifter_nickname = Column(String(20))

    # 赠送状态
    _pending = Column('pending', SmallInteger, default=1)

    @property
    def pending(self):
        """
        使外部能以字段的形式获取到对应的枚举值
        :return:
        """
        return PendingStatus(self._pending)

    @pending.setter
    def pending(self, status):
        """
        使外部能以枚举值的形式对pending进行赋值
        :param status:
        :return:
        """
        self._pending = status.value
