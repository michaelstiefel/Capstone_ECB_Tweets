import pandas as pd
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.model_selection import train_test_split, GridSearchCV
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import TweetTokenizer
from sklearn.feature_extraction.text import CountVectorizer
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
import nltk
nltk.download('omw-1.4')
import string
import re
import pickle
from wordcloud import WordCloud


## Read in data and do elementary cleaning
df = pd.read_pickle("./webapp/data/df_tweets.pkl")
df = df.set_index(pd.to_datetime(df['created_at']))

df = df.sort_index().loc['2021-01-01':'2021-12-31']
#df = df.sort_index().loc['2021-01-01':'2021-01-15']

# Remove cricket-related tweets
df = df[~df['all_text'].str.contains('cricket', case=False, regex=False)]


# Split data into training and test set for model evaluation
X_train, X_test = train_test_split(df['all_text'].values, random_state = 42, test_size = 0.05)


url_regex = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
punct = list(string.punctuation)
stopword_list = stopwords.words('english') + punct + ['rt', 'via', '…', '..', 'ecb', '’', '@ecb',
'central', 'bank', '1x', 'easycopbots', 'schuldensuehner', 'like', 'urlplaceholder',
'easycop', 'users', '“', 'ecb\'s', '...', 'profklausschwab', 'amp', 'robinmonotti']







vect = CountVectorizer(stop_words=stopword_list, max_df=0.1, max_features=5000)

search_params = {'n_components': [4, 6, 8]}

lda_instance = LatentDirichletAllocation()

print("Fitting count vectorizer")
model_vect = vect.fit_transform(X_train)
holdout_model_vect = vect.transform(X_test)
print("Fitting LDA")
lda = GridSearchCV(lda_instance, param_grid=search_params)
lda.fit(model_vect)
print("Fitting LDA done")
print(lda.best_params_)
number_of_topics = lda.best_params_['n_components']

model_filepath = "./webapp/model/lda"
print(f"Save model to {model_filepath}")
pickle.dump(lda, open(model_filepath, 'wb'))

feature_names = vect.get_feature_names_out()

n_top_words = 10

for topic_idx, topic in enumerate(lda.components_):
    print(f"Topic {topic_idx + 1}")
    print(" ".join([feature_names[i] for i in topic.argsort()[:-n_top_words - 1: -1]]))

# Model evaluation
# Training data
training_loglikelihood = lda.score(model_vect)
training_perplexity = lda.perplexity(model_vect)

# Holdout data
holdout_loglikelihood = lda.score(holdout_model_vect)
holdout_perplexity = lda.perplexity(holdout_model_vect)

print("Training data:")
print(f"Training loglikelihood {training_loglikelihood}")
print(f"Training perplexity {training_perplexity}")

print("Test data:")
print(f"Holdout loglikelihood {holdout_loglikelihood}")
print(f"Holdout perplexity {holdout_perplexity}")


## Draw Word Cloud


def draw_word_cloud(index):
    imp_words_topic=""
    comp=lda.components_[index]
    vocab_comp = zip(feature_names, comp)
    sorted_words = sorted(vocab_comp, key= lambda x:x[1], reverse=True)[:15]
    for word in sorted_words:
        imp_words_topic=imp_words_topic+" "+word[0]

    wordcloud = WordCloud(width=600, height=400).generate(imp_words_topic)
    plt.figure( figsize=(5,5))
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout()
    plt.savefig("./Figures/wordcloud_topic_{}".format(index+1))

for i in range(number_of_topics):
    draw_word_cloud(i)
