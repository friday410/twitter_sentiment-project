#Import the necessary methods from tweepy library
# from pyes import *
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import sys
import boto3
import botocore.session
import json
import traceback
#from builtins import print

#Variabl: that contains the user credentials to access Twitter API 
access_token = '931455098-4cheNDFrVVjEqEwyqMEYdIfUznEUP0OZolsGvTeb'
access_token_secret = 'SGJc2RsyyTnhP2RGvLeYniNzRC0sswhxmIIeoaNVsFcoL'
consumer_key = 'jaCwGEBj0rGWkwMqwyGCgfk7q'
consumer_secret = 'joFq8o1BPPIiNmlYMbcZKSa7YcO0W2SspyDagReTsMUfQzRPGK'

# queue = None
sqs = boto3.resource('sqs')
# queue = sqs.create_queue(QueueName='tweetsQueue', Attributes={'Keyword': None, 'longitude': None, 'latitude':None, 'message': None})
# queue = sqs.create_queue(QueueName='tweetsQueue1', Attributes={'DelaySeconds':'5'})
queue = sqs.get_queue_by_name(QueueName='tweetsQueue2')

# conn = None
keywordList = None
message_id = 0

class StdOutListener(StreamListener):
    # print 'Getting tweets'
    def on_data(self, data):
        global message_id

        data = json.loads(data)
        try:
            if('text' and 'coordinates' in data and data['coordinates']):
                lo = float(data['coordinates']['coordinates'][0])
                la = float(data['coordinates']['coordinates'][1])
                user_text = str(data['text'].encode("utf8"))

                for word in keywordList:
                    if word in data['text']:
                        print 'word exist'
                        print word
                        
                        # response = queue.send_messages(Entries=[
                        #   {
                        #       'Id': str(message_id),
                        #       'MessageBody': str(message_id) + user_text,
                        #       'MessageAttributes': {

                        #           'Keyword':{
                        #               'StringValue': word,
                        #               'DataType':'String'
                        #           },

                        #           'longitude':{
                        #               'StringValue': str(lo),
                        #               'DataType':'String'
                        #           },

                        #           'latitude':{
                        #               'StringValue': str(la),
                        #               'DataType':'String'
                        #           },

                        #           'message':{
                        #               'StringValue': user_text,
                        #               'DataType':'String'
                        #           }

                        #       }
                        #   }
                        # ])

                        response = queue.send_message(
                            MessageBody = 'boto3', 
                            MessageAttributes = {

                                'KeywordTweet':{
                                    'StringValue': str(word),
                                    'DataType':'String'
                                },

                                'longitude':{
                                    'StringValue': str(lo),
                                    'DataType':'String'
                                },

                                'latitude':{
                                    'StringValue': str(la),
                                    'DataType':'String'
                                },

                                'message':{
                                    'StringValue': user_text,
                                    'DataType':'String'
                                }

                            }
                        )
                        message_id = message_id + 1
                        
                        print(response.get('MessageId'))
                        print(response.get('MD5OfMessageBody'))
                        print(response.get('Failed'))
                        

                        #conn.refresh()
                        # conn.index({"key":word, "longitude": lo, "latitude": la}, "test-index", "test-type")
        except:
            traceback.print_exc()
            print 'except passed on outer loop'
            

        return True     
    def on_error(self, status):
        print >> sys.stderr, 'Error with status code:', status_code


if __name__ == '__main__':
    # conn.indices.put_mapping("test-type", {'properties':mapping}, ["test-index"])
    keywordList = ['happy','breakfast','cry','love','rain','suck','music','relax','angry','secret']
    #This is a basic listener that just prints received tweets to stdout.

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    GEOBOX_WORLD = [-130,-60,70,60]
    stream.filter(locations=GEOBOX_WORLD)
    stream.filter(languages=["en"])
    print('EXECUTED MAIN IN ELASTIC PUT DATA')


    # sqs = boto3.resource('sqs')
    # queue = sqs.create_queue(QueueName='tweetsQueue', Attributes={'Keyword': '0', 'longitude': '0', 'latitude':'0', 'message': '0'})

