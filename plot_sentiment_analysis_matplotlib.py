import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime

### Load data

df = pd.read_pickle("./data/df_tweets.pkl")
df = df.set_index(pd.to_datetime(df['created_at']))
print(df.info())
print(df.head())



sentiment = df['compound'].resample('W').mean().fillna(0)

idx = pd.DatetimeIndex(df['created_at'])
ones = np.ones(len(idx))

number_series = pd.Series(ones, index= idx)
number = number_series.resample('W').sum().fillna(0)

fig, ax = plt.subplots(2, 1, sharex = True)



# Define time range
datemin = datetime(2020, 10, 25, 0, 0)
datemax = datetime(2021, 11, 15, 0, 0)

ax[0].set_xlim(datemin, datemax)


max_freq_numbers = number.max()
ax[0].set_ylim(0, max_freq_numbers + 5000)

ax[0].set_title("Tweet Frequencies")
ax[1].set_title("Tweet Average Sentiment")

ax[0].plot(number.index, number)
ax[1].plot(sentiment.index, sentiment)



plt.show()
