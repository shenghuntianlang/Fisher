"""
the viewmodel for book
"""


class BookViewModel:
    """
    handle the single data
    """

    def __init__(self, book):
        self.title = book['title']
        # use '、' to connect the elements of list
        self.author = '、'.join(book['author'])
        self.publisher = book['publisher']
        self.price = book['price']
        # if current key's value of data is none,
        # put the empty string in this key, or put the original value in it.
        self.pages = book['pages'] or ""
        self.isbn = book['isbn']
        self.summary = book['summary'] or ""
        self.image = book['image']
        self.pubdate = book['pubdate']
        self.binding = book['binding']

    @property
    def intro(self):
        """
        use '/' to reformat the introduce which include author,publisher,price
        if one of them is null, this funcation can remove it.
        :return:
        """
        intro_afterfilter = filter(lambda x: True if x else False,
                                   [self.author, self.publisher, self.price])
        return '/'.join(intro_afterfilter)


class BookCollection:
    """
    handle serval datas
    """

    def __init__(self):
        self.total = 0
        self.books = []
        self.keyword = ''

    def fill(self, yushu_book, keywork):
        """
        use BookViewModel to fill final books data
        :param yushu_book:
        :param keywork:
        :return:
        """
        self.total = yushu_book.total
        self.keyword = keywork
        self.books = [BookViewModel(book) for book in yushu_book.books]


class _BookViewModel:
    @classmethod
    def package_single(cls, data, keywork):
        """
        Reorganizing for result where the search keywork type is isbn
        :param data:    the search result
        :param keywork:
        :return:    the reorganized result
        """
        returned = {
            'books': [],
            'total': 0,
            'keywork': keywork
        }
        if data:
            returned['total'] = 1
            returned['books'] = [cls.__cut_book_data(data)]
        return returned

    @classmethod
    def package_collection(cls, data, keywork):
        """
        Reorganizing for result where the search keywork type is book's name
        :param data:    the search result
        :param keywork:
        :return:    the reorganized result
        """
        returned = {
            'books': [],
            'total': 0,
            'keywork': keywork
        }
        if data:
            returned['total'] = data['total']
            returned['books'] = [cls.__cut_book_data(book) for book in data['books']]
        return returned

    @classmethod
    def __cut_book_data(cls, data):
        """
        The reusable funcation for cut book data
        :param data     the books in data
        :return:    books after reorganized
        """
        book = {
            'title': data['title'],
            # use '、' to connect the elements of list
            'author': '、'.join(data['author']),
            'publisher': data['publisher'],
            'price': data['price'],
            # if current key's value of data is none,
            # put the empty string in this key, or put the original value in it.
            'pages': data['pages'] or "",
            'summary': data['summary'] or "",
            'image': data['image']
        }
        return book
