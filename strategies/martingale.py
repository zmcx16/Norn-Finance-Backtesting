import logging
from datetime import datetime
import backtrader as bt

import indicators as nfb_ind


class Martingale(bt.Strategy):
    params = dict(
        period=252,
        trade_size=0.05,
        min_positions=(
            (0, 0.2, "#bdbdbd"),
            (0.05, 0.4, "#9e9e9e"),
            (0.1, 0.6, "#757575"),
            (0.15, 0.8, "#616161"),
            (0.2, 1.0, "#424242"),
        ),
    )

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        logging.info('%s %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.data_close = self.datas[0].close

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

        self.hl_list = []
        for mp in self.p.min_positions:
            self.hl_list.append(
                nfb_ind.HighLine(self.datas[0], period=self.p.period, rate=mp[0], color=mp[2])
            )

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        self.log('Close: %.2f Value: %d Cash: %d' % (self.data_close[0], self.broker.getvalue(), self.broker.get_cash()))
        if self.order:
            return

        pos = self.broker.getvalue() - self.broker.get_cash()
        pos_r = pos / self.broker.getvalue()

        trade_size = 0
        for i in range(len(self.p.min_positions)):
            if self.data_close[0] < self.hl_list[i][0]:
                if pos_r < self.p.min_positions[i][1]:
                    trade_size = int(self.broker.getvalue() * self.p.trade_size / self.data_close[0])
                    self.log('+Close: %.2f(%.2f) pos: %.2f, pos_r: %.2f (%.2f), trade_size:%d' %
                             (self.data_close[0], self.hl_list[i][0], pos, pos_r, self.p.min_positions[i][1], trade_size))

        for i in reversed(range(len(self.p.min_positions))):
            if self.data_close[0] > self.hl_list[i][0]:
                if i < len(self.p.min_positions)-1 and pos_r > self.p.min_positions[i+1][1]:
                    trade_size = -1 * int(self.broker.getvalue() * self.p.trade_size / self.data_close[0])
                    self.log('-Close: %.2f(%.2f) pos: %.2f, pos_r: %.2f (%.2f), trade_size:%d' %
                             (self.data_close[0], self.hl_list[i][0], pos, pos_r, self.p.min_positions[i][1], trade_size))

        if trade_size > 0:
            self.log('BUY CREATE: %.2f * %d' % (self.data_close[0], trade_size))
            self.order = self.buy(size=trade_size)
        elif trade_size < 0:
            self.log('SELL CREATE: %.2f * %d' % (self.data_close[0], trade_size))
            self.order = self.sell(size=trade_size)

        """
        # Check if we are in the market
        if not self.position:

            # Not yet ... we MIGHT BUY if ...
            if self.dataclose[0] > self.sma[0]:

                # BUY, BUY, BUY!!! (with all possible default parameters)
                self.log('BUY CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()

        else:

            if self.dataclose[0] < self.sma[0]:
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log('SELL CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()
        """
