import os
from pathlib import Path

import pandas as pd
import lightgbm as lgb
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split, TimeSeriesSplit, GroupKFold
import numpy as np

from FinanceData import get_finance_data


def rsi(df, n=14):
    close = df["Close"]
    delta = close.diff()[1:]

    prices_up = delta.copy()
    prices_down = delta.copy()

    prices_up[prices_up < 0] = 0
    prices_down[prices_down > 0] = 0

    roll_up = prices_up.rolling(n).mean()
    roll_down = prices_down.abs().rolling(n).mean()

    rs = roll_up / roll_down
    rsi = 100.0 - (100.0 / (1.0 + rs))

    return rsi


import pandas as pd


def create_features(df):
    df = df.drop(columns=["Open", "High", "Low", "Adj Close"])

    df["EMA_9"] = df["Close"].ewm(9).mean().shift()

    sma_periods = [5, 10, 20, 30, 60]

    for period in sma_periods:
        df[f"SMA_{period}"] = df["Close"].rolling(period).mean().shift()

    df["RSI"] = rsi(df).fillna(0)

    EMA_12 = pd.Series(df["Close"].ewm(span=12, min_periods=12).mean())
    EMA_26 = pd.Series(df["Close"].ewm(span=26, min_periods=26).mean())

    df["MACD"] = pd.Series(EMA_12 - EMA_26)
    df["MACD_signal"] = pd.Series(df.MACD.ewm(span=9, min_periods=9).mean())

    df = df.loc[df.index >= "2001-01-01"]

    return df


def train(df):
    train_df = df.loc[df.index < "2018-01-01"].copy()
    valid_df = df.loc[("2018-01-01" <= df.index) & (df.index < "2019-07-01")].copy()
    test_df = df.loc[("2019-07-01" <= df.index) & (df.index < "2021-01-01")].copy()

    y_train = train_df["Close"].copy()
    X_train = train_df.drop(["Close"], axis=1)

    y_valid = valid_df["Close"].copy()
    X_valid = valid_df.drop(["Close"], axis=1)

    y_test = test_df["Close"].copy()
    X_test = test_df.drop(["Close"], axis=1)

    lgb_train = lgb.Dataset(X_train, label=y_train)
    lgb_valid = lgb.Dataset(X_valid, label=y_valid, reference=lgb_train)
    lgb_test = lgb.Dataset(X_test, label=y_test)

    param = {
        "n_estimators": 1000,
        "force_col_wise": "true",
        "objective": "regression",
        "boosting": "gbdt",
        "learning_rate": 0.01,
        "num_leaves": 48,
        "min_data_in_leaf": 40,
        "tree_learner": "serial",
        "device_type": "cpu",
        "seed": 100,
        "max_depth": 12,
        "metric": "l2",
        "verbose": 0,
    }

    tss = TimeSeriesSplit(5)
    folds = tss.split(X_train)
    cv_res_gen = lgb.cv(param, lgb_train, folds=folds, callbacks=[lgb.early_stopping(20)])
    cv_res_obj = lgb.cv(param, lgb_train, folds=tss, callbacks=[lgb.early_stopping(20)])

    np.testing.assert_allclose(cv_res_gen["l2-mean"], cv_res_obj["l2-mean"])
    
    model = lgb.train(param, lgb_train, lgb_valid, callbacks=[lgb.early_stopping(100)])
    
    predict_train = model.predict(X_train)
    predict_test = model.predict(X_test)
    
    mse = mean_squared_error(y_test, predict_test)
    r2 = r2_score(y_test, predict_test)
    
    final_result = pd.concat([y_test.reset_index(drop=True), pd.DataFrame(predict_test)], axis=1)
    final_result.columns = ['Label', 'Predict']
    final_result.index = y_test.index
    
    return final_result


def process(ticker):
    path = (Path(__file__).parent / f"./data/stock/{ticker}-train.csv").resolve()
    
    result = 0
    
    if not os.Path(path).is_file():
        df = get_finance_data(ticker)
        df.drop("Date", inplace=True, axis=1)
        df = create_features(df)

        result = train(df)
    
        result.to_csv(path, sep=",")
    else:
        result = pd.read_csv(path)
    
    return result.to_json()