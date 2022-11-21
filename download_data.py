import os
import pathlib
import logging

import argparse
import yfinance as yf


if __name__ == "__main__":

    root = pathlib.Path(__file__).parent.resolve()

    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "-symbol", dest="symbol", default="SPY")
    parser.add_argument("-o", "-output-folder-path", dest="output_folder_path", default=str(root / "datas"))
    parser.add_argument("-l", "-log-level", dest="log_level", default="DEBUG")
    args = parser.parse_args()

    logging.basicConfig(level=args.log_level)

    if not os.path.exists(args.output_folder_path):
        os.makedirs(args.output_folder_path)

    ticker = yf.Ticker(args.symbol)
    hist = ticker.history(period="max")
    hist.reset_index(inplace=True)
    hist['Date'] = hist['Date'].dt.strftime('%Y-%m-%d')
    output = hist.to_csv(lineterminator="\n", index=False)
    with open(pathlib.Path(args.output_folder_path) / (args.symbol + '.csv'), 'w', encoding='utf-8') as f:
        f.write(output)

    logging.info('all task done')
