import json
import os
from datetime import date, datetime
from pathlib import Path
import ssl

import pandas as pd
import FinanceDataReader as fdr


_STOCK_DATA_PATH = (Path(__file__).parent / "./data/stock").resolve()
_CRYPTO_DATA_PATH = (Path(__file__).parent / "./data/stock").resolve()


def _get_filepath(crypto=False, metadata=False):
    extension = "json" if type == "metadata" else "csv"
    path = _CRYPTO_DATA_PATH if crypto else _STOCK_DATA_PATH

    def closure(ticker):
        return (path / f"{ticker}.{extension}").resolve()

    return closure


_stock_data_path = _get_filepath()
_stock_metadata_path = _get_filepath(False, True)
_crypto_data_path = _get_filepath(True)
_crypto_metadata_path = _get_filepath(True, True)


def get_finance_data(ticker):
    if not os.path.exists(_STOCK_DATA_PATH):
        os.makedirs(_STOCK_DATA_PATH)

    df = pd.DataFrame()
    should_update_metadata = False
    metadata_filepath = (_STOCK_DATA_PATH / f"{ticker}.json").resolve()
    data_filepath = (_STOCK_DATA_PATH / f"{ticker}.csv").resolve()

    if not Path(data_filepath).is_file():
        df = _create_data(data_filepath, ticker)
        _update_metadata(metadata_filepath, ticker)

    else:
        with open(metadata_filepath, "r") as f_json:
            metadata = json.load(f_json)

            if metadata["lastModified"] != f"{date.today()}":
                _update_data(data_filepath, ticker, metadata["lastModified"])
                should_update_metadata = True

        if should_update_metadata:
            _update_metadata(metadata_filepath, ticker)

        df = pd.read_csv(data_filepath)

    df = df.interpolate()
    df.index = pd.to_datetime(df["Date"])

    return df


def get_crypto_data(ticker):
    """
    cryptodatadownload.com의 시간봉 데이터를 가져옴
    제공 데이터 -> 비트/이더/리플/링크/라이트/에이다/이오스/빗캐/유니/스시/폴카닷/븐브/테조스/트론
    columns = ['Open','High','Low','Close','Volume']
    """

    if not os.path.exists():
        os.makedirs(_CRYPTO_DATA_PATH)

    df = pd.DataFrame()
    should_update_metadata = False

    if not Path(_crypto_data_path(ticker)).is_file():
        df = _create_data(ticker)
        should_update_metadata = True
    else:
        with open(_crypto_metadata_path(ticker), "r", encoding="utf-8") as f_json:
            metadata = json.load(f_json)

            if metadata["lastModified"] != f"{datetime.now()}":
                _update_crypto_data(ticker, metadata["lastModified"])
                should_update_metadata = True

        df = pd.read_csv(_crypto_data_path(ticker))

    if should_update_metadata:
        _update_crypto_metadata(ticker)

    return df


def _update_metadata(path_to_file, ticker):
    with open(path_to_file, "w", encoding="utf-8") as f:
        metadata = {"ticker": ticker, "lastModified": f"{date.today()}"}

        json.dump(metadata, f, sort_keys=True, indent=2, ensure_ascii=False)


def _create_data(path_to_file, ticker):
    with open(path_to_file, "x", encoding="utf-8"):
        pass

    df = fdr.DataReader(ticker, "2000-01-01", date.today())
    df.to_csv(path_to_file, sep=",", na_rep="NaN")

    return df


def _update_data(path_to_file, ticker, last_modified):
    df = fdr.DataReader(ticker, last_modified, date.today())
    df.to_csv(path_to_file, sep=",", na_rep="NaN", mode="a", header=False)


def _get_crypto_metadata(ticker):
    with open(_crypto_metadata_path(ticker), "r", encoding="utf-8") as f:
        return json.loads(f)


def _update_crypto_metadata(ticker):
    with open(_crypto_metadata_path(ticker), "w", encoding="utf-8") as f:
        metadata = {"ticker": ticker, "lastModified": f"{date.today()}"}

        json.dump(metadata, f, sort_keys=True, indent=2, ensure_ascii=False)


def _fetch_crypto_data(ticker):
    ssl._create_default_https_context = ssl._create_unverified_context
    url = "https://www.cryptodatadownload.com/cdd/FTX_Futures_" + ticker.split("-")[0] + "PERP_1h.csv"
    df = pd.read_csv(url)
    df = df.reset_index()
    df.columns = df.iloc[0]
    df = df.iloc[1:]
    df = df.set_index("date")
    df.rename(index={"date", "Datetime"})
    df.index = pd.to_datetime(df.index)
    df = df[["open", "high", "low", "close", "Volume USDT"]]
    df.columns = ["Open", "High", "Low", "Close", "Volume"]
    df = df[::-1]
    df = df.astype("float")

    return df


def _create_crypto_data(ticker):
    with open(_crypto_data_path(ticker), "x", encoding="utf-8"):
        pass

    df = _fetch_crypto_data(ticker)

    df.to_csv(_crypto_data_path(ticker), sep=",", na_rep="NaN")

    return df


def _update_crypto_data(ticker, last_modified):
    df = _fetch_crypto_data(ticker).loc[df.index >= last_modified]

    df.to_csv(_crypto_data_path(ticker), sep=",", na_rep="NaN", mode="a", header=False)
