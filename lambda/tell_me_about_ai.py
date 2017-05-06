import json
import logging
import boto3
import random

"""
Lambda function that reads a file from S3 and prints out a random quote from the file
"""

"""
Global variables
"""
S3_BUCKET = 'ai8j4f8jfjf8jfjfjfjfjfa'
S3_OBJECT = 'quotes.txt'


def close(fulfillment_state, message):

    response = {
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }

    return response


def get_quote():

    s3_client = boto3.client('s3')
    download_file = '/tmp/quotes.txt'
    s3_client.download_file(S3_BUCKET, S3_OBJECT, download_file)
    lines = open(download_file).read().splitlines()
    q = random.choice(lines)
    return q


def answer_question(intent_request):

    q = get_quote()
    return close(
        'Fulfilled',
        {
            'contentType': 'PlainText',
            'content': q
        }
    )


""" --- Intents --- """


def dispatch(intent_request):

    intent_name = intent_request['currentIntent']['name']

    if intent_name == 'answerwithquote':
        return answer_question(intent_request)
    raise Exception('Intent with name ' + intent_name + ' not supported')


""" --- Main handler --- """


def lambda_handler(event, context):
    return dispatch(event)
