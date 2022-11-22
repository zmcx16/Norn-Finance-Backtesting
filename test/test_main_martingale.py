import os
import json
from types import SimpleNamespace

import main_martingale


def test_main():
    output_path = './temp/test_result.json'
    if os.path.exists(output_path):
        os.remove(output_path)

    args = SimpleNamespace()
    args.log_level = "INFO"
    args.data = "./datas/SPY.csv"
    args.output_path = './temp/test_result.json'
    args.from_date = "1999-01-01"
    args.to_date = "2021-12-31"
    args.plot = "0"
    args.type = "1"
    args.period = "252"
    args.trade_size = "0.05"
    args.position_error = "0.05"
    args.min_position_list = ""

    main_martingale.main(args)
    assert os.path.exists(output_path)
    with open(output_path, 'r', encoding='utf-8') as f:
        report = json.loads(f.read())
        assert report.get('strategy_name') is not None, "strategy_name not found"
        assert report.get('strategy_param') is not None, "strategy_param not found"
        assert report.get('returns') is not None, "returns not found"
        assert report.get('annual_return') is not None, "annual_return not found"
        assert report.get('cumulative_return') is not None, "cumulative_return not found"
        assert report.get('sharp_ratio') is not None, "sharp_ratio not found"
        assert report.get('draw_down') is not None, "draw_down not found"

    os.remove(output_path)
