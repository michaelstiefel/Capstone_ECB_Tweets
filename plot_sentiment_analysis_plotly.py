import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime

### Load data

df = pd.read_pickle("./data/df_tweets.pkl")
df = df.set_index(pd.to_datetime(df['created_at']))

weekly = df['compound'].resample('W').mean().fillna(0)

fig = px.line(data_frame=weekly, x=weekly.index, y=weekly, title="test")

# Create buttons
#fin_buttons = [
#  {'count': 7, 'label': "1WTD", 'step': "day", 'stepmode': "todate"},
#  {'count': 6, 'label': "6MTD", 'step': "month", 'stepmode': "todate"},
#  {'count': 1, 'label': "YTD", 'step': "year", 'stepmode': "todate"}
#]

# Create the date range buttons & show the plot
#fig.update_layout({'xaxis': {'rangeselector': {'buttons': fin_buttons}}})
fig.show()
