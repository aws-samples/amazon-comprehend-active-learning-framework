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
kinesis_delivery_stream = os.environ['kinesis_delivery_stream']

def lambda_handler(event, context):
    #print(event)
    body = json.loads(event['body'])
    classifier = body['classifier']
    sentence = body['sentence']
    
    try:
        lowconfidencepair = {}
        lowconfidencepair['utterance']=sentence
        lowconfidencepair['prediction']='CLASSIFY'
        lowconfidencepair['confidence']='NONE'
        lowconfidencepair['classifier']=classifier
        lowconfidencepair = json.dumps(lowconfidencepair)+"\n"
    
        # write the lowconfidencepair to firehose
        kinesis.put_record(DeliveryStreamName=kinesis_delivery_stream,Record={"Data":bytes(lowconfidencepair, 'utf-8')})
        
    except Exception as e: 
        print(e)
           
   
    print('Success')
    return {'statusCode': 200,'headers' :  {"X-Requested-With": '*',"Access-Control-Allow-Headers": 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,x-requested-with',"Access-Control-Allow-Origin": '*',"Access-Control-Allow-Methods": 'DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT'},'body': 'success'}
