import pandas as pd
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.model_selection import train_test_split
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


## Read in data and do elementary cleaning
df = pd.read_pickle("./webapp/data/df_tweets.pkl")
df = df.set_index(pd.to_datetime(df['created_at']))

df = df.sort_index().loc['2021-01-01':'2021-12-31']
#df = df.sort_index().loc['2021-01-01':'2021-03-01']

df = df[~df['all_text'].str.contains('cricket', case=False, regex=False)]

X_train, X_test = train_test_split(df['all_text'].values, random_state = 42, test_size = 0.1)


url_regex = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
punct = list(string.punctuation)
stopword_list = stopwords.words('english') + punct + ['rt', 'via', '…', '..', 'ecb', '’', '@ecb',
'central', 'bank', '1x', 'easycopbots', 'schuldensuehner', 'like', 'urlplaceholder',
'easycop', 'users', '“', 'ecb\'s', '...', 'profklausschwab', 'amp']

def process_tweets(text, tokenizer=TweetTokenizer(), lemmatizer=WordNetLemmatizer(), stopwords=stopword_list):
    """
    Lowercase, tokenize tweets, remove stopwords, lemmatize
    """

    # Remove urls
    detected_urls = re.findall(url_regex, text)
    for url in detected_urls:
        text = text.replace(url, "urlplaceholder")
    text = text.lower()
    tokens = tokenizer.tokenize(text)


    clean_tokens = [my_tok for my_tok in tokens if my_tok not in stopwords and not my_tok.isdigit()]

    lemmatized_tokens = []
    for tok in clean_tokens:
        clean_tok = lemmatizer.lemmatize(tok).lower().strip()
        clean_tokens.append(clean_tok)

    return clean_tokens

#tweet_tokenizer = TweetTokenizer()
#lemmatizer = WordNetLemmatizer()



vect = CountVectorizer(stop_words=stopword_list, max_df=0.1, max_features=5000)

lda = LatentDirichletAllocation(n_components = 7)

print("Fitting count vectorizer")
model_vect = vect.fit_transform(X_train)
holdout_model_vect = vect.transform(X_test)
print("Fitting LDA")
lda.fit(model_vect)
print("Fitting LDA done")

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
