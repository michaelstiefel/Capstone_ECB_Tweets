import configparser
import boto3
import json
import pandas as pd
import pickle
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer


config = configparser.ConfigParser()
config.read("capstone_project.cfg")

AWS_ACCESS_KEY_ID =config['AWS']['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = config['AWS']['AWS_SECRET_ACCESS_KEY']
S3_BUCKET = config['AWS']['S3_BUCKET_INPUT']

s3 = boto3.client("s3", aws_access_key_id=AWS_ACCESS_KEY_ID,
                         aws_secret_access_key=AWS_SECRET_ACCESS_KEY)


sid = SentimentIntensityAnalyzer()

def list_of_files():
    s3_resource = boto3.resource('s3')
    my_bucket = s3_resource.Bucket(S3_BUCKET)
    summaries = my_bucket.objects.all()
    files = []
    for file in summaries:
        # this prints the bucket object
        #print("Object: {}".format(summaries))
        #print(file.key)
        files.append(file.key)
        # file.key is supposed to return the names of the list of objects
        # print(file.key)
    return files


#response = s3.list_objects(Bucket = S3_BUCKET)

def flatten_tweets(tweets_json):
    """ Flatten tweets and keep important columns."""
    tweets_list = []
    fields_to_keep = ['id', 'created_at', 'lang',
    'text', 'retweeted_status_text', 'all_text', 'quoted_status_text',
     # Aditional user information
    'user_screen_name','user_description', 'user_followers_count', 'user_friends_count',
    'user_id', 'user_verified', 'user_created_at',
     # Additional retweet information
    'retweeted_status_id', 'retweeted_status_user_id',
    'retweeted_status_user_screen_name', 'retweeted_status_user_description',
    'retweeted_status_user_followers_count', 'retweeted_status_user_friends_count',
    'retweeted_status_user_verified', 'retweeted_status_user_created_at',
    # Additional quoted status information
    'quoted_status_id', 'quoted_status_user_id',
    'quoted_status_user_screen_name', 'quoted_status_user_description',
    'quoted_status_user_followers_count', 'quoted_status_user_friends_count',
    'quoted_status_user_verified', 'quoted_status_user_created_at']

    # Iterate through each tweet
    for tweet in tweets_json:

        tweet_obj = json.loads(tweet)

        # Store user information
        tweet_obj['user_screen_name'] = tweet_obj['user']['screen_name']

        tweet_obj['user_description'] = tweet_obj['user']['description']

        tweet_obj['user_followers_count'] = tweet_obj['user']['followers_count']

        tweet_obj['user_friends_count'] = tweet_obj['user']['friends_count']

        tweet_obj['user_id'] = tweet_obj['user']['id']

        tweet_obj['user_verified'] = tweet_obj['user']['verified']

        tweet_obj['user_created_at'] = tweet_obj['user']['created_at']

        # Check if this is a 140+ character tweet
        if 'extended_tweet' in tweet_obj:
            # Store the extended tweet text in text
            tweet_obj['text'] = tweet_obj['extended_tweet']['full_text']
        else:
            tweet_obj['text'] = tweet_obj['text']

        if 'retweeted_status' in tweet_obj:
            # Store user and tweet information of the retweet
            tweet_obj['retweeted_status_user_screen_name'] = tweet_obj['retweeted_status']['user']['screen_name']
            tweet_obj['retweeted_status_user_description'] = tweet_obj['retweeted_status']['user']['description']
            tweet_obj['retweeted_status_user_followers_count'] = tweet_obj['retweeted_status']['user']['followers_count']
            tweet_obj['retweeted_status_user_friends_count'] = tweet_obj['retweeted_status']['user']['friends_count']
            tweet_obj['retweeted_status_user_id'] = tweet_obj['retweeted_status']['user']['id']
            tweet_obj['retweeted_status_user_verified'] = tweet_obj['retweeted_status']['user']['verified']
            tweet_obj['retweeted_status_user_created_at'] = tweet_obj['retweeted_status']['user']['created_at']
            tweet_obj['retweeted_status_id'] = tweet_obj['retweeted_status']['id']
            # Store the retweet text in 'retweeted_status-text'
            if 'extended_tweet' in tweet_obj['retweeted_status']:
                tweet_obj['retweeted_status_text'] = tweet_obj['retweeted_status']['extended_tweet']['full_text']
            else:
                tweet_obj['retweeted_status_text'] = tweet_obj['retweeted_status']['text']
        else:
            tweet_obj['retweeted_status_user_screen_name'] = None
            tweet_obj['retweeted_status_user_description'] = None
            tweet_obj['retweeted_status_user_followers_count'] = None
            tweet_obj['retweeted_status_user_friends_count'] = None
            tweet_obj['retweeted_status_user_id'] = None
            tweet_obj['retweeted_status_id'] = None
            tweet_obj['retweeted_status_user_verified'] = None
            tweet_obj['retweeted_status_user_created_at'] = None
            tweet_obj['retweeted_status_text'] = None


        if 'quoted_status' in tweet_obj:
            # Store user and tweet information of the quoted tweet
            tweet_obj['quoted_status_user_screen_name'] = tweet_obj['quoted_status']['user']['screen_name']
            tweet_obj['quoted_status_user_description'] = tweet_obj['quoted_status']['user']['description']
            tweet_obj['quoted_status_user_followers_count'] = tweet_obj['quoted_status']['user']['followers_count']
            tweet_obj['quoted_status_user_friends_count'] = tweet_obj['quoted_status']['user']['friends_count']
            tweet_obj['quoted_status_user_id'] = tweet_obj['quoted_status']['user']['id']
            tweet_obj['quoted_status_user_verified'] = tweet_obj['quoted_status']['user']['verified']
            tweet_obj['quoted_status_user_created_at'] = tweet_obj['quoted_status']['user']['created_at']
            tweet_obj['quoted_status_id'] = tweet_obj['quoted_status']['id']
            # Store the retweet text in 'retweeted_status-text'
            if 'extended_tweet' in tweet_obj['quoted_status']:
                tweet_obj['quoted_status_text'] = tweet_obj['quoted_status']['extended_tweet']['full_text']
            else:
                tweet_obj['quoted_status_text'] = tweet_obj['quoted_status']['text']

            tweet_obj['all_text'] = tweet_obj['text'] + " " + tweet_obj['quoted_status_text']
        else:
            tweet_obj['quoted_status_user_screen_name'] = None
            tweet_obj['quoted_status_user_description'] = None
            tweet_obj['quoted_status_user_followers_count'] = None
            tweet_obj['quoted_status_user_friends_count'] = None
            tweet_obj['quoted_status_user_id'] = None
            tweet_obj['quoted_status_id'] = None
            tweet_obj['quoted_status_user_verified'] = None
            tweet_obj['quoted_status_user_created_at'] = None
            tweet_obj['quoted_status_text'] = None

            tweet_obj['all_text'] = tweet_obj['text']





        tweet_obj = {key_to_keep: tweet_obj[key_to_keep] for key_to_keep in fields_to_keep }


        tweets_list.append(tweet_obj)


    return pd.DataFrame(tweets_list)


files = list_of_files()

all_dfs = []


for file in files:
    print(file)
    obj = s3.get_object(Bucket = S3_BUCKET, Key = file)
    obj_body = obj['Body'].read().decode('utf-8')
    try:
        df = flatten_tweets(obj_body.splitlines())
        df['sentiment_scores'] = df['all_text'].apply(lambda tweet: sid.polarity_scores(tweet))
        df['compound']  = df['sentiment_scores'].apply(lambda score_dict: score_dict['compound'])
        df = df[['id', 'created_at', 'all_text', 'compound']]
        all_dfs.append(df)
    except:
        continue

df_tweets = pd.concat(all_dfs)
print(df_tweets.head())
print(df_tweets.info())
df_tweets.to_csv('./data/tweets_and_sentiment.csv')

with open('./data/df_tweets.pkl', 'wb') as f:
    pickle.dump(df_tweets, f)


#list_of_tweets = []
#list_year_month = [('2020', '10'), ('2020', '11'), ('2020', '12'), ('2021', '01')]
#list_year_month = [('2020', '10'), ('2020', '11'), ('2020', '12'), ('2021', '01'), ('2021', '02')]
#for year, month in list_year_month:
#    prefix = "./{0}/{1}/".format(year,month)

#    response = s3.list_objects(Bucket = S3_BUCKET, Prefix = prefix)
#    counter = 0

#    for file in response['Contents']:
    #local_path = "Temp/" + str(counter) +".json"
    #s3.download_file(Bucket = S3_BUCKET, Key = file['Key'], Filename = local_path)
#        obj = s3.get_object(Bucket = S3_BUCKET, Key = file['Key'])
#        counter += 1
#        print(counter)
#        print(file['Key'])

#        obj_body = obj['Body'].read().decode('utf-8')
#        list_of_tweets.append(flatten_tweets(obj_body.splitlines()))
#        #time.sleep(1)

#df_tweets = pd.concat(list_of_tweets)


#print(df_tweets.info())



#print(df_tweets.head())
#print(df_tweets['text'].values[:5])

#df_tweets.to_csv("./ECB_Tweets/df_tweets.csv",
#                index = False,
#                header = True,
#                sep="|",
#                chunksize = 100000,
#                encoding = 'utf-8'
#)


    #    list_of_tweets.append(tweet)
    #    print(len(list_of_tweets)).head()
    #list_of_json_files.append(list_of_tweets)
