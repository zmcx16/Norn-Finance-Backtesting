import os
import pathlib
import logging

import argparse
import yfinance as yf


if __name__ == "__main__":

    root = pathlib.Path(__file__).parent.resolve()
    data_folder = root / "datas"
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "-symbol", dest="symbol", default="SPY")
    parser.add_argument("-l", "-log-level", dest="log_level", default="DEBUG")
    args = parser.parse_args()

    logging.basicConfig(level=args.log_level)

    ticker = yf.Ticker(args.symbol)
    hist = ticker.history(period="max")
    hist.reset_index(inplace=True)
    hist['Date'] = hist['Date'].dt.strftime('%Y-%m-%d')
    output = hist.to_csv(lineterminator="\n", index=False)
    with open(data_folder / (args.symbol + '.csv'), 'w', encoding='utf-8') as f:
        f.write(output)

    logging.info('all task done')
