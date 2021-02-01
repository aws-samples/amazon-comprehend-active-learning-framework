# Copyright Amazon.com, Inc. and its affiliates. All Rights Reserved.
#   SPDX-License-Identifier: MIT
  
#   Licensed under the MIT License. See the LICENSE accompanying this file
#   for the specific language governing permissions and limitations under
#   the License.

import json
import boto3
from urllib.parse import unquote_plus
import urllib
import time
import os

region = os.environ['AWS_REGION']

client = boto3.client(service_name='comprehend', region_name=region, use_ssl=True)
training_bucket = os.environ['train_bucket']
s3 = boto3.resource('s3')
kinesis = boto3.client('firehose')

kinesis_delivery_stream = os.environ['human_review_firehose']

def lambda_handler(event, context):
    
    # Get the object from the event
    bucketName = event['Records'][0]['s3']['bucket']['name']
    keyName = unquote_plus(event['Records'][0]['s3']['object']['key'])
    fileName = keyName[keyName.rindex('/')+1:keyName.rindex('.')]
    
    print(f"Bucket: {bucketName} key:{keyName} file:{fileName}")

    # Read the S3 Object
    bucket = s3.Bucket(bucketName)
    body = bucket.Object(keyName).get()['Body'].read().decode("utf-8", 'ignore')
    
    # split the body by period to get individual sentences
    body = json.loads(body)
    print(body)
    humanReviewedAnswers = body['humanAnswers'][0]['answerContent']
    feedbackitems = body['inputContent']['comprehendPredictions']
    keys = humanReviewedAnswers.keys()
    print(keys)
    output = ""
    for item, answer in zip(feedbackitems, humanReviewedAnswers):
        utterance = item['utterance']
        prediction = humanReviewedAnswers[answer]
        output = output + prediction + ",\"" + utterance +"\"\n"
    output  = output[:-1]

    kinesis.put_record(DeliveryStreamName=kinesis_delivery_stream,Record={"Data":bytes(output, 'utf-8')})
    
    print(output)

    return 0
