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


kinesis = boto3.client('firehose')
s3 = boto3.resource('s3')

kinesis_delivery_stream = os.environ['kinesis_delivery_stream']

def lambda_handler(event, context):
    #print(event)
    print("Reading batch feedback file")
    # Get the object from the event
    bucketName = event['Records'][0]['s3']['bucket']['name']
    keyName = unquote_plus(event['Records'][0]['s3']['object']['key'])

    # Read the S3 Object
    bucket = s3.Bucket(bucketName)
    body = bucket.Object(keyName).get()['Body'].read().decode("utf-8", 'ignore')

    print('Splitting file for rows')    
    
    body = json.loads(body)
    
    classifier = body['classifier']
    sentences = body['sentences']
    
    try:
        for sentence in sentences:
            lowconfidencepair = {}
            lowconfidencepair['utterance']=sentence
            lowconfidencepair['prediction']='CLASSIFY'
            lowconfidencepair['confidence']='NONE'
            lowconfidencepair['classifier']=classifier
            lowconfidencepair = json.dumps(lowconfidencepair)+"\n"
            print("Low confidence Pair")
            print(lowconfidencepair)
            # write the lowconfidencepair to firehose
            kinesis.put_record(DeliveryStreamName=kinesis_delivery_stream,Record={"Data":bytes(lowconfidencepair, 'utf-8')})
        
    except Exception as e: 
        print(e)
           
   
    print('Success')
    return {'statusCode': 200,'headers' :  {"X-Requested-With": '*',"Access-Control-Allow-Headers": 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,x-requested-with',"Access-Control-Allow-Origin": '*',"Access-Control-Allow-Methods": 'DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT'},'body': 'success'}
