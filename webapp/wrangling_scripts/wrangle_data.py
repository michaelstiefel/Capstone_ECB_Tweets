import pandas as pd
import plotly.graph_objs as go
import numpy as np
import sys
import string
from collections import Counter
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords

# Read in data for tweets and filter for 2021
df = pd.read_pickle("./data/df_tweets.pkl")
df = df.set_index(pd.to_datetime(df['created_at']))
df = df.loc['2021-01-01':'2021-12-31']

df = df[~df['all_text'].str.contains('cricket', case=False, regex=False)]

# Read in ecb event data and filter for 2021
ecb_events = pd.read_csv("./data/ecb_decision_dates.csv", index_col='date', parse_dates=True)
ecb_events = ecb_events.sort_index().loc['2021-01-01':'2021-12-31']
event_dates = ecb_events.index.tolist()

# Preprocess tweet data to generate wordcount

def process_tweets(text, tokenizer=TweetTokenizer(), stopwords=[]):
    """
    Lowercase, tokenize tweets, remove stopwords
    """
    text = text.lower()
    tokens = tokenizer.tokenize(text)
    return [my_tok for my_tok in tokens if my_tok not in stopwords and not my_tok.isdigit()]

tweet_tokenizer = TweetTokenizer()
punct = list(string.punctuation)
stopword_list = stopwords.words('english') + punct + ['rt', 'via', '…', '..', 'ecb', 'lagarde', '’', '@lagarde', '@ecb',
'central', 'bank', '1x', '@easycopbots', 'european', 'euro', 'christine', 'digital', '#ecb', 'president', 'bitcoin',
'@schuldensuehner', 'like', 'england', 'world', 'would', 'pakistan', 'one', 'time', 'people', 'last', 'said', 'good',
'#bitcoin', 'today', 'says', '💥', 'easycop', 'us', 'users', '“', 'ecb\'s', '...', 'new', '@profklausschwab', 'also', 'want']

tf = Counter()

for index, row in df.iterrows():
    tokens = process_tweets(text = row['all_text'], tokenizer = tweet_tokenizer, stopwords = stopword_list)
    tf.update(tokens)
most_common_tags = []
counts_of_most_common_tags = []
for tag, count in tf.most_common(50):
    print("{0}: {1}".format(tag,count))
    most_common_tags.append(tag)
    counts_of_most_common_tags.append(count)


# Compute number of daily tweets
idx = df.index
ones = np.ones(len(idx))

number_series = pd.Series(ones, index = idx)

daily_number = number_series.resample('D').sum().fillna(0)

daily = df['compound'].resample('D').mean().fillna(0)
monthly = df['compound'].resample('4W').mean().fillna(0)

def return_figures():
    """Creates four plotly visualizations

    Args:
        None

    Returns:
        list (dict): list containing the four plotly visualizations

    """

    # first chart plots arable land from 1990 to 2015 in top 10 economies
    # as a line chart

    graph_one = []
    graph_one.append(
      go.Scatter(
      x = daily_number.index,
      y = daily_number,
      mode='lines')
    )

    layout_one = dict(title = 'Daily Number of Tweets',
                xaxis = dict(title = 'Day'),
                yaxis = dict(title = 'Number of Tweets'),
                )

# second chart plots ararble land for 2015 as a bar chart
    graph_two = []

    graph_two.append(
      go.Scatter(
      x = daily.index,
      y = daily,
      mode='lines')
    )

    layout_two = dict(title = 'Avg. Daily Sentiment',
                xaxis = dict(title = 'Day',),
                yaxis = dict(title = 'Sentiment'),
                )


# third chart plots percent of population that is rural from 1990 to 2015
    graph_three = []
    graph_three.append(
      go.Histogram(
      x = df['compound'])
    )

    layout_three = dict(title = 'Distribution of Sentiment Scores',
                xaxis = dict(title = 'Sentiment Score'),
                yaxis = dict(title = 'Frequency')
                       )

# fourth chart shows rural population vs arable land
    graph_four = []

    graph_four.append(
      go.Bar(
      x = most_common_tags,
      y = counts_of_most_common_tags)
      )

    layout_four = dict(title = 'Most common words',
                xaxis = dict(title = 'Word'),
                yaxis = dict(title = 'Frequency'),
                )

    # append all charts to the figures list
    figures = []

    figure_one = go.Figure(
        data=graph_one,
        layout=layout_one)

    for date in event_dates:
        figure_one.add_vline(x=date, line_width=1, line_dash="dash", line_color="red")
    figures.append(figure_one)

    figure_two = go.Figure(
         data=graph_two,
         layout=layout_two)

    for date in event_dates:
        figure_two.add_vline(x=date, line_width=1, line_dash="dash", line_color="red")
    figures.append(figure_two)

    figure_three = go.Figure(
         data=graph_three,
         layout=layout_three)
    figures.append(figure_three)

    figure_four = go.Figure(
         data=graph_four,
         layout=layout_four)
    figures.append(figure_four)

    return figures
