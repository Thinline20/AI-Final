from datetime import datetime
import FinanceDataReader as fdr

import csv
import json

def get_data(ticker):
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")

    with open(f"data/raw-{ticker}.json", "rw") as f_json:
        metadata = json.load(f_json)

        if (metadata["lastModified"] == today)

        with open(f"data/raw-{ticker}.csv") as f_csv:
            pass

def update_data(ticker, last_modified="2001-01-01"):
    df = fdr.DataReader(ticker, last_modified)

    with open(f"raw-{ticker}.csv", "w", encoding="utf-8", newline="\n"):
        pass

kospi_df = fdr.DataReader("KS11", "2001-01-01", "2001-02-01")