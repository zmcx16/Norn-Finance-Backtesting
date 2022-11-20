import logging
from enum import Enum
import backtrader as bt

import indicators as nfb_ind


class MartingaleType(float, Enum):
    Martingale = 1.0
    AntiMartingale = -1.0


class Martingale(bt.Strategy):
    params = dict(
        type=MartingaleType.Martingale,
        period=252,
        trade_size=0.05,
        position_error=0.1,
        min_positions=(
            (0, 0.2, "#29b6f6"),
            (0.05, 0.4, "#03a9f4"),
            (0.1, 0.6, "#039be5"),
            (0.15, 0.8, "#0288d1"),
            (0.2, 1.0, "#0277bd"),
        ),
    )

    def debug_log(self, txt):
        logging.debug('%s %s' % (self.datas[0].datetime.date(0).isoformat(), txt))

    def info_log(self, txt):
        logging.info('%s %s' % (self.datas[0].datetime.date(0).isoformat(), txt))

    def __init__(self, param):
        self.bar_executed = None
        if param is not None:
            for name, val in param.items():
                setattr(self.params, name, val)

        self.data_close = self.datas[0].close

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

        self.line_list = []
        for mp in self.p.min_positions:
            if self.p.type == MartingaleType.Martingale:
                self.line_list.append(nfb_ind.HighLine(self.datas[0], period=self.p.period, rate=mp[0], color=mp[2]))
            elif self.p.type == MartingaleType.AntiMartingale:
                self.line_list.append(nfb_ind.LowLine(self.datas[0], period=self.p.period, rate=mp[0], color=mp[2]))

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.info_log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.info_log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.info_log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.info_log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        if self.order:
            return
        pos = self.broker.getvalue() - self.broker.get_cash()
        pos_r = pos / self.broker.getvalue()

        self.info_log(
            'Close: %.2f Value: %d Cash: %d Position: %.2f' % (self.data_close[0], self.broker.getvalue(),
                                                               self.broker.get_cash(), pos_r * 100))

        trade_size = 0
        for i in range(len(self.p.min_positions)):
            if self.data_close[0] * self.p.type < self.line_list[i][0] * self.p.type:
                if pos_r < self.p.min_positions[i][1] - self.p.position_error:
                    trade_size = int(self.broker.getvalue() * self.p.trade_size / self.data_close[0])
                    self.debug_log('+Close: %.2f(%.2f) pos: %.2f, pos_r: %.2f (%.2f), trade_size:%d' %
                                   (self.data_close[0], self.line_list[i][0], pos, pos_r, self.p.min_positions[i][1],
                                    trade_size))

        for i in reversed(range(len(self.p.min_positions))):
            if self.data_close[0] * self.p.type > self.line_list[i][0] * self.p.type:
                if pos_r > self.p.min_positions[i][1] + self.p.position_error:
                    trade_size = -1 * int(self.broker.getvalue() * self.p.trade_size / self.data_close[0])
                    self.debug_log('-Close: %.2f(%.2f) pos: %.2f, pos_r: %.2f (%.2f), trade_size:%d' %
                                   (self.data_close[0], self.line_list[i][0], pos, pos_r, self.p.min_positions[i][1],
                                    trade_size))

        if trade_size > 0:
            self.info_log('BUY CREATE: %.2f * %d' % (self.data_close[0], trade_size))
            self.order = self.buy(size=trade_size)
        elif trade_size < 0:
            self.info_log('SELL CREATE: %.2f * %d' % (self.data_close[0], trade_size))
            self.order = self.sell(size=trade_size)
