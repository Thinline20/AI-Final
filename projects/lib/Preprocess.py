#%%
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeRegressor
import pandas as pd
import FinanceDataReader as fdr

from FinanceData import get_finance_data

#%%
colors = [
    "#ef4444",
    "#f97316",
    "#f59e0b",
    "#eab308",
    "#84cc16",
    "#22c55e",
    "#10b981",
    "#14b8a6",
    "#06b6d4",
    "#0ea5e9",
    "#3b82f6",
    "#6366f1",
    "#8b5cf6",
    "#a855f7",
    "#d946ef",
    "#ec4899",
    "#f43f5e",
]


def rgb_to_float(rgb):
    r = int(rgb[1:3], 16) / 255.0
    g = int(rgb[3:5], 16) / 255.0
    b = int(rgb[5:7], 16) / 255.0

    return (r, g, b)


color_pal = list(map(rgb_to_float, colors))

#%%

raw_data = get_finance_data("ks11")
raw_data.head()

df = raw_data[["Close"]]

#%%
df.plot(figsize=(15, 5), color=color_pal[0], title="ks11")

#%%
# Train/Test split
X_train = df.loc[df.index < "2019-01-01"]
X_test = df.loc[df.index >= "2019-01-01"]

#%%
fix, ax = plt.subplots(figsize=(15, 5))
X_train.plot(ax=ax, label="Train set", color=color_pal[0], title="Data Train/Test split")
X_test.plot(ax=ax, label="Test set", color=color_pal[10])
ax.axvline("2019-01-01", color="black", ls="--")
plt.show()

# %%
six_month_data = df.loc[(df.index > "2010-01-01") & (df.index <= "2010-06-30")]
six_month_data.plot(figsize=(15, 5), title="Week of Data from 2010-01-01 to 2010-01-31", color=color_pal[6])
plt.plot()

# %%
# Feature Creation

#%%
# Crypto Data
