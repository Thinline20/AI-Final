#%%
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeRegressor
import seaborn as sns
import pandas as pd
import FinanceDataReader as fdr

from FinanceData import get_finance_data

#%%
color_pal = sns.color_palette()

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
X_test.plot(ax=ax, label="Test set", color=color_pal[1])
ax.axvline("2019-01-01", color="black", ls="--")
plt.show()

# %%
six_month_data = df.loc[(df.index > "2010-01-01") & (df.index <= "2010-06-30")]
six_month_data.plot(figsize=(15, 5), title="Week of Data from 2010-01-01 to 2010-01-31")
plt.plot()

# %%
# Feature Creation

#%%
# Crypto Data