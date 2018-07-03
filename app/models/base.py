# 实例化sqlalchemy对象
from contextlib import contextmanager
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from sqlalchemy import Column, SmallInteger, Integer


class SQLAlchemy(_SQLAlchemy):
    """
    重写SQLAlchemy类,使用contextmanager增加auto_commit方法
    实现自动为执行代码添加异常捕获并抛出功能
    """

    @contextmanager
    def auto_commit(self):
        try:
            # yield 参考生成器,程序执行到此会中断,开始执行with上下文中的代码,
            # 直到从上下文中退出,才会继续执行下面的代码
            yield
            self.session.commit()
        except Exception as ex:
            self.session.rollback()
            raise ex


class Query(BaseQuery):
    """
    重写filter_by,加入默认字典元素status
    """

    def filter_by(self, **kwargs):
        if 'status' not in kwargs.keys():
            kwargs['status'] = 1
        return super(Query, self).filter_by(**kwargs)


db = SQLAlchemy(query_class=Query)


class Base(db.Model):
    """
    自定义基类,可以使基类继承db的Model实例, 此后继承自此类的类遍无需继承db的Model实例
    """
    __abstract__ = True
    create_time = Column('create_time', Integer)

    # 数据是否为删除状态,默认为否
    status = Column(SmallInteger, default=1)

    def __init__(self):
        """
        实例化子类时获取实例化的时间
        """
        self.create_time = datetime.now().timestamp()

    def set_attrs(self, attr_dicts):
        """
        dynamic assign
        :param attr_dicts:
        :return:
        """
        for key, value in attr_dicts.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)

    @property
    def create_datetime(self):
        """
        将int型的时间转换为时间对象
        :return:
        """
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        else:
            return None

    def delete(self):
        self.status = 0
