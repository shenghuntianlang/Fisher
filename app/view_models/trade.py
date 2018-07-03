"""
the View Model for trade info
"""
from app.view_models.book import BookViewModel


class TradeInfo:
    def __init__(self, goods):
        self.total = 0
        self.trades = []
        self.__parse(goods)

    def __parse(self, goods):
        self.total = len(goods)
        self.trades = [self.__map_to_trade(single) for single in goods]

    def __map_to_trade(self, single):
        time = single.create_datetime.strftime('%Y-%m-%d') if single.create_datetime else '未知'
        return dict(
            user_name=single.user.nickname,
            time=time,
            id=single.id
        )


class MyTrades:
    """
    the base view model for my gifts or my wishes
    """

    def __init__(self, trades_of_mine, re_trades_count_list):
        self.trades = []

        self.__trades_of_mine = trades_of_mine
        self.__re_trades_count_list = re_trades_count_list
        self.trades = self.__parse()

    def __parse(self):
        temp_trades = []
        for trade in self.__trades_of_mine:
            my_trade = self.__matching(trade)
            temp_trades.append(my_trade)
        return temp_trades

    def __matching(self, trade):
        count = 0
        for re_trade_count in self.__re_trades_count_list:
            if trade.isbn == re_trade_count['isbn']:
                count = re_trade_count['count']
        r = {
            're_trades_count': count,
            'book': BookViewModel(trade.book),
            'id': trade.id
        }
        return r
