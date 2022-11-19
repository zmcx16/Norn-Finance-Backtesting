from datetime import datetime
import backtrader as bt

import strategies as ndf_strats


if __name__ == '__main__':

    cerebro = bt.Cerebro()
    cerebro.addstrategy(ndf_strats.Martingale)

    data0 = bt.feeds.GenericCSVData(
        dataname="./datas/SPY.csv",
        fromdate=datetime(2010, 1, 1),
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
