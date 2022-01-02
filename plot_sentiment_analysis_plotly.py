#import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from datetime import datetime

### Load data

df = pd.read_pickle("./data/df_tweets.pkl")
df = df.set_index(pd.to_datetime(df['created_at']))

weekly = df['compound'].resample('W').mean().fillna(0)

fig = go.Figure()

graph_one = go.Scatter(x=weekly.index, y=weekly, mode='lines')

layout_one = dict(title = 'Chart One',
                xaxis = dict(title = 'x-axis label'),
                yaxis = dict(title = 'y-axis label'),
                )

fig.add_trace(graph_one)
#fig = dict(data = graph_one, layout = layout_one)

fig.show()
