from datetime import datetime
import backtrader as bt


class SmaCross(bt.SignalStrategy):
    def __init__(self):
        sma1, sma2 = bt.ind.SMA(period=10), bt.ind.SMA(period=30)
        crossover = bt.ind.CrossOver(sma1, sma2)
        self.signal_add(bt.SIGNAL_LONG, crossover)


if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.addstrategy(SmaCross)

    data0 = bt.feeds.GenericCSVData(
        dataname="../datas/SPY.csv",
        fromdate=datetime(2021, 1, 1),
        todate=datetime(2021, 10, 31),
        nullvalue=0.0,
        dtformat='%Y-%m-%d',
        tmformat='%H.%M.%S',
        datetime=0,
        time=-1,
        high=2,
        low=3,
        open=1,
        close=4,
        volume=5,
        openinterest=-1)
    cerebro.adddata(data0)

    # Set the commission
    cerebro.broker.setcommission(commission=0.0)

    cerebro.run()
    cerebro.plot()
