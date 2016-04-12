import boto3
import boto.sns
from alchemyapi import AlchemyAPI

alchemyapi = AlchemyAPI()

sqs = boto3.resource('sqs')
client = boto3.client('sns')
queue = sqs.get_queue_by_name(QueueName='tweetsQueue2')
def send_message(mes):
    try:
        REGION = 'us-east-1'
        TOPIC = '###############################'
        conn = boto.sns.connect_to_region(REGION)
        conn.publish(topic = TOPIC, message=mes)
    except:
        print "Failed to send a message"
        
while True:
    print 'while'
    for message in queue.receive_messages(MessageAttributeNames=['KeywordTweet', 'longitude', 'latitude', 'message'], MaxNumberOfMessages = 10):
        print message.message_attributes.get('KeywordTweet')
        print message.message_attributes
        myText = message.message_attributes.get('message').get('StringValue')
        response = alchemyapi.sentiment("text", myText)
        print 'response before if', response
        if "docSentiment" in response:
            print 'response: ', response
            print "Sentiment: ", response["docSentiment"]["type"]
            mes = message.message_attributes.get('KeywordTweet').get('StringValue') + ' ' + message.message_attributes.get('longitude').get('StringValue') + ' ' + message.message_attributes.get('latitude').get('StringValue') + ' ' + str(response["docSentiment"]["type"])
            send_message(mes)
        # print message.body
        message.delete()
