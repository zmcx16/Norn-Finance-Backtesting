import logging
import argparse
from datetime import datetime
import backtrader as bt
import backtrader.analyzers as btanalyzers

import strategies as ndf_strats


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "-log-level", dest="log_level", default="INFO")
    parser.add_argument("-from", "-from-date", dest="from_date", default="2015-01-01")
    parser.add_argument("-to", "-to-date", dest="to_date", default="2021-10-31")
    args = parser.parse_args()

    logging.basicConfig(level=args.log_level)

    cerebro = bt.Cerebro()
    cerebro.addstrategy(ndf_strats.Martingale)

    cerebro.broker.setcommission()
    cerebro.addanalyzer(btanalyzers.AnnualReturn, _name='annual_return')
    cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='sharp_ratio')

    data0 = bt.feeds.GenericCSVData(
        dataname="./datas/SPY.csv",
        fromdate=datetime.strptime(args.from_date, '%Y-%m-%d'),
        todate=datetime.strptime(args.to_date, '%Y-%m-%d'),
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

    thestrats = cerebro.run()
    thestrat = thestrats[0]

    logging.info(thestrat.analyzers.annual_return.get_analysis())
    logging.info(thestrat.analyzers.sharp_ratio.get_analysis())

    cerebro.plot()
