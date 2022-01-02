from flask import Flask

app = Flask(__name__)

from ecb_sentiment import routes
