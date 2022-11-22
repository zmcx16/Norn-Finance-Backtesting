import os
import pathlib

import download_data


def test_main():
    symbol = "SPY"
    output_folder_path = "./temp"
    output_path = pathlib.Path(output_folder_path) / (symbol + '.csv')
    if os.path.exists(output_path):
        os.remove(output_path)

    download_data.main(symbol, output_folder_path, "INFO")
    assert os.path.exists(output_path), "%s file not found" % output_path
    os.remove(output_path)
