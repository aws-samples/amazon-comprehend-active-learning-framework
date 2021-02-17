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


client = boto3.client(service_name='comprehend', region_name=os.environ['AWS_REGION'], use_ssl=True)
kinesis = boto3.client('firehose', region_name=os.environ['AWS_REGION'])
ssm = boto3.client('ssm', region_name=os.environ['AWS_REGION'])

kinesis_delivery_stream = os.environ['kinesis_delivery_stream']

comprehend_endpoint = os.environ['comprehend_endpoint_name']
ssm_key_name = os.environ['ssm_key_name'] or ''
score_threshold = os.environ['score_threshold']




def lambda_handler(event, context):
    print(event)
    body = json.loads(event['body'])
    
    classifier = body['classifier']
    sentence = body['sentence']
    
    if not ssm_key_name:
        comprehend_endpoint_arn = comprehend_endpoint
    else:
        parameter = ssm.get_parameter(Name=ssm_key_name)
        comprehend_endpoint_arn = parameter['Parameter']['Value']



    endpointArn = comprehend_endpoint_arn
    print(endpointArn)


    try:
        response = client.classify_document(Text=sentence,EndpointArn=endpointArn)
        p = response['Classes'][0]['Name']
        score = response['Classes'][0]['Score']
        #print(f"S:{sentence}, Score:{score}")
        response = {}
        response['utterance']=sentence
        response['prediction']=p
        response['confidence'] = score
        
        lowconfidencepair = response
        lowconfidencepair['classifier']=classifier
        score_threshold_float = float(score_threshold)
        lowconfidencepair = json.dumps(lowconfidencepair)+"\n"

        if score < score_threshold_float:
            # write the low-confidence-pair to firehose
            kinesis.put_record(
                DeliveryStreamName=kinesis_delivery_stream,
                Record={"Data":bytes(lowconfidencepair, 'utf-8')})
            
        return {'statusCode': 200,'headers' :  {"X-Requested-With": '*',"Access-Control-Allow-Headers": 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,x-requested-with',"Access-Control-Allow-Origin": '*',"Access-Control-Allow-Methods": 'DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT'},'body': json.dumps(response)}
    
    except Exception as e: 
        print(e)
           
   
    print('Failed')
    return {'statusCode': 200,'headers' :  {"X-Requested-With": '*',"Access-Control-Allow-Headers": 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,x-requested-with',"Access-Control-Allow-Origin": '*',"Access-Control-Allow-Methods": 'DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT'},'body': 'failed'}
