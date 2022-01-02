# Capstone Project: Twitter Sentiment about the European Central Bank

## Introduction

This project is part of the Udacity Data Scientist Nanodegree Program. Its purpose is to create a flask web app to illustrate insights from tweets about the European Central Bank (ECB) in 2021. Specifically, the following questions will be addressed:

- How does Twitter Sentiment about the European Central Bank change over time?
- Does Twitter Sentiment change on days when the ECB decided on its monetary policy?
- What are the topics discussed by users on Twitter and how do they change over time?

## Data

Two data sources are used for the web app:

- A dataset of tweets that extracted tweets mentioning the European Central Bank from Twitter and that is stored in a AWS S3 Bucket
- A dataset of ECB policy events scraped from the ECB website

## Files

- read_tweets_and_extract_sentiment.py

This file reads and cleans the tweets. It flattens and converts the tweets from json files into a pandas dataframe. To this end, it collapses all tweet text columns (text of the tweet, quoted tweet, retweeted tweet, etc) into a single column. This column is then used for a sentiment analysis. To perform the sentiment analysis, the VADER sentiment analysis tool (https://github.com/cjhutto/vaderSentiment) is used. This tool is part of the nltk library and specifically designed to analyse social media.

- capstone_project.default.cfg

This config file should be filled with the AWS credentials and the name of the AWS S3 bucket

## How to execute the analysis

1. Complete the AWS credentials with your credentials, fill out the name of the AWS S3 bucket and save the file as capstone_project.cfg

2. Run read_tweets_and_extract_sentiment.py: This generates the data as a pickle (and also csv file) in the folder webapp/data

3. Run ecb_sentiment_app.py in the webapp folder.

## Results

## Conclusions and directions for future research
