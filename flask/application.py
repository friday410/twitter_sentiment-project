from os import environ, system
from datetime import datetime
from flask import render_template, jsonify, Flask, request
# from TwitterMapProj import app
#from elasticsearch import ElasticSearch
# from pyes import *
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import requests
import json

from pyes import *

#conn = ES('127.0.0.1:9200')
# conn = ES('172.31.53.200:9200')

application = app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST', 'PUT'])
def home():
    """Renders the home page."""
    global conn
    try:
        data = json.loads(request.data)
        print data
        message = data['Message']
        print 'MESSAGE = ' + message
        tokens = message.split(' ')
        print tokens
        # COULD BE WRONG HERE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        conn.index({"key":tokens[0], "longitude": tokens[1], "latitude": tokens[2], "senti": tokens[3]}, "test-index", "test-type")
        print tokens
    except:
        print 'INSIDE OF THE EXCEPTION'

    return render_template(
        'mainTwitterMap.html',
        title='Main Twitter Map Page',
        year=datetime.now().year,
    )

@app.route('/getTwits/<keyword>')
def get_tweets(keyword):
    global conn
    keyword = keyword.encode('utf-8')
    data = []

    print 'BEFORE TERM QUERY'
    q = TermQuery('key', keyword)
    print 'AFTER TERM QUERY'
    results = conn.search(query = q)
    print len(results)

    for line in results:
        data.append(line)
        print line
    return jsonify({'data':data})

if __name__ == '__main__':

    conn = ES('172.31.53.200:9200')
    #conn = ES('54.172.248.22:9200')
    try:
        conn.indices.delete_index('test-index')
    except:
        pass
    conn.indices.create_index('test-index')
    mapping = {
        'key': {
            'store':'yes',
            'type': 'string'
        },

        'longitude': {
            'store': 'yes',
            'type':'float'
        },

        'latitude': {
            'store': 'yes',
            'type':'float'
        }
    }
    conn.indices.put_mapping("test-type", {'properties':mapping}, ["test-index"])

    app.run(debug=True, host='0.0.0.0')
