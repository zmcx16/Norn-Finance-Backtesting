import sys
import json
import logging
import argparse
from datetime import datetime
import numpy as np
import backtrader as bt
import backtrader.analyzers as btanalyzers

import strategies as ndf_strats


def main(args):
    logging.basicConfig(level=args.log_level)

    # parse strategy type
    stype = None
    if args.type == "1":
        stype = ndf_strats.MartingaleType.Martingale
    elif args.type == "-1":
        stype = ndf_strats.MartingaleType.AntiMartingale

    if stype is None:
        logging.error("Not support strategy")
        sys.exit()

    # parse strategy min_position_list
    min_positions = [
        [0, 0.2, "#29b6f6"],
        [0.05, 0.4, "#03a9f4"],
        [0.1, 0.6, "#039be5"],
        [0.15, 0.8, "#0288d1"],
        [0.2, 1.0, "#0277bd"],
    ]
    if args.min_position_list != "" and "," in args.min_position_list:
        min_positions = []
        lines = args.min_position_list.split(";")
        for line in lines:
            p = line.split(",")
            min_positions.append([float(p[0]), float(p[1]), p[2]])
    else:
        logging.warning("parse parameter failed, use default min_position_list")

    strategy_param = dict(
        type=stype,
        period=int(args.period),
        trade_size=float(args.trade_size),
        position_error=float(args.position_error),
        min_positions=min_positions
    )

    cerebro = bt.Cerebro()
    cerebro.addstrategy(ndf_strats.Martingale, strategy_param)

    cerebro.broker.setcommission()
    cerebro.addanalyzer(btanalyzers.Returns, _name='returns')
    cerebro.addanalyzer(btanalyzers.AnnualReturn, _name='annual_return')
    cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='sharp_ratio')
    cerebro.addanalyzer(btanalyzers.DrawDown, _name='draw_down')

    data0 = bt.feeds.GenericCSVData(
        dataname=args.data,
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

    results = cerebro.run()
    result = results[0]

    returns = result.analyzers.returns.get_analysis()
    output = {
        "strategy_name": stype.name,
        "strategy_param": strategy_param,
        "returns": returns,
        "annual_return": result.analyzers.annual_return.get_analysis(),
        "cumulative_return": float(np.exp(np.cumsum(returns["rtot"])) - 1),
        "sharp_ratio": result.analyzers.sharp_ratio.get_analysis(),
        "draw_down": result.analyzers.draw_down.get_analysis().max
    }

    logging.info("******* %s result *******" % stype.name)
    logging.info("Log Return: %s" % output["returns"])
    logging.info("Annual Return: %s" % output["annual_return"])
    logging.info("Cumulative Return: {0:.2%}".format(output["cumulative_return"]))
    logging.info("Draw Down: %s" % output["draw_down"])
    logging.info("Sharp Ratio: %s" % output["sharp_ratio"])

    with open(args.output_path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(output, indent=4))

    if args.plot == "1":
        cerebro.plot()

    logging.info('all task done')


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "-log-level", dest="log_level", default="INFO")
    parser.add_argument("-d", "-data", dest="data", default="./datas/SPY.csv")
    parser.add_argument("-o", "-output-path", dest="output_path", default="./result.json")
    parser.add_argument("-from", "-from-date", dest="from_date", default="1999-01-01")
    parser.add_argument("-to", "-to-date", dest="to_date", default="2021-12-31")
    parser.add_argument("-plot", "-plot", dest="plot", default="1")
    parser.add_argument("-t", "-type", dest="type", default="1")
    parser.add_argument("-p", "-period", dest="period", default="252")
    parser.add_argument("-s", "-trade-size", dest="trade_size", default="0.05")
    parser.add_argument("-e", "-position-error", dest="position_error", default="0.05")
    parser.add_argument("-mpl", "-min-position-list", dest="min_position_list", default="")
    main(parser.parse_args())
