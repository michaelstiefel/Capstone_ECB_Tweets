#import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from datetime import datetime

### Load data

df = pd.read_pickle("./webapp/data/df_tweets.pkl")
df = df.set_index(pd.to_datetime(df['created_at']))

ecb_events = pd.read_csv("./webapp/data/ecb_decision_dates.csv", index_col='date', parse_dates=True)
ecb_events = ecb_events.loc['2021-01-01':'2021-12-31']
event_dates = ecb_events.index.tolist()
print(event_dates)


daily = df['compound'].resample('D').mean().fillna(0)



fig = go.Figure()

graph_one = go.Scatter(x=daily.index, y=daily, mode='lines')

layout_one = dict(title = 'Chart One',
                xaxis = dict(title = 'x-axis label'),
                yaxis = dict(title = 'y-axis label'),
                )

fig.add_trace(graph_one)

for date in event_dates:
    fig.add_vline(x=date, line_width=1, line_dash="solid", line_color="red")

#fig = dict(data = graph_one, layout = layout_one)

fig.show()
