import json
import os
from datetime import date
from pathlib import Path

import pandas as pd
import FinanceDataReader as fdr


def get_data(ticker):
    data_path = (Path(__file__).parent / "./data").resolve()
    if not os.path.exists(data_path):
        os.makedirs(data_path)

    should_update_metadata = False
    # metadata_filepath = f"./data/raw-{ticker}.json"
    metadata_filepath = (data_path / f"./raw-{ticker}.json").resolve()
    data = pd.DataFrame()
    # data_filepath = f"./data/raw-{ticker}.csv"
    data_filepath = (data_path / f"./raw-{ticker}.csv").resolve()

    if not Path(data_filepath).is_file():
        data = _create_data(data_filepath, ticker)
        _update_metadata(metadata_filepath, ticker)

        return data

    with open(metadata_filepath, "r") as f_json:
        metadata = json.load(f_json)

        if metadata["lastModified"] != date.today():
            _update_data(data_filepath, ticker, metadata["lastModified"])
            should_update_metadata = True

    if should_update_metadata:
        _update_metadata(metadata_filepath, ticker)

    data = pd.read_csv(data_filepath)

    return data


def _update_metadata(path_to_file, ticker):
    with open(path_to_file, "w", encoding="utf-8") as f:
        metadata = {"ticker": ticker, "lastModified": f"{date.today()}"}

        json.dump(metadata, f, sort_keys=True, indent=2, ensure_ascii=False)


def _create_data(path_to_file, ticker):
    with open(path_to_file, "x", encoding="utf-8"):
        pass

    df = fdr.DataReader(ticker, "2001-01-01", date.today())
    df.to_csv(path_to_file, sep=",", na_rep="NaN")

    return df


def _update_data(path_to_file, ticker, last_modified):
    df = fdr.DataReader(ticker, last_modified, date.today())
    df.to_csv(path_to_file, sep=",", na_rep="NaN", mode="a", header=False)
