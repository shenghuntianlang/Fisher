"""
the book search opearation for fisher
"""
from flask import current_app

from app.libs.httper import Http


class YuShuBook:
    isbn_url = 'http://t.yushu.im/v2/book/isbn/{}'
    keyword_url = 'http://t.yushu.im/v2/book/search?q={}&count={}&start={}'

    def __init__(self):
        self.total = 0
        self.books = []

    # 将传入的参数加入请求连接,可以使用字符串的格式化函数format,函数会根据传入的次序将数据填入
    # '{}'中,或者可以对格式化操作进行次序调整
    def search_by_isbn(self, isbn):
        url = self.isbn_url.format(isbn)
        result = Http.get(url)
        self.__fill_single(result)

    def search_by_keyword(self, keyword, page=1):
        url = self.keyword_url.format(keyword, current_app.config['PER_PAGE'],
                                      self.__get_start_page(page))
        result = Http.get(url)
        self.__fill_collection(result)

    def __fill_single(self, data):
        if data:
            self.total = 1
            self.books.append(data)

    def __fill_collection(self, data):
        if data:
            self.total = data['total']
            self.books = data['books']

    def __get_start_page(self, page):
        return (page - 1) * current_app.config['PER_PAGE']

    @property
    def first(self):
        """
        获取书籍列表中的第一本书
        @property装饰器用以使方法能以属性访问的方式调用
        :return:
        """
        return self.books[0] if self.total >= 1 else None
