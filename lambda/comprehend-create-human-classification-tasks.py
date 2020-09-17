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

s3 = boto3.resource('s3')
a2i = boto3.client('sagemaker-a2i-runtime')

flowDefnARN = unquote_plus(os.environ['FLOW_DEF_ARN']) 


def lambda_handler(event, context):
    #print(event)
    print("Creating human review taks")

    # Get the object from the event
    bucketName = event['Records'][0]['s3']['bucket']['name']
    keyName = unquote_plus(event['Records'][0]['s3']['object']['key'])
    fileName = keyName[keyName.rindex('/')+1:]
   
    # Read the S3 Object
    bucket = s3.Bucket(bucketName)
    body = bucket.Object(keyName).get()['Body'].read().decode("utf-8", 'ignore')

    categories = os.environ['categories']

    if not categories:
        raise Exception('The environment variable categories cannot be empty')

    rowCount = 0

    print('Splitting file for pairs')    
    
    sentences = body.split("\n")
    
    # Create the human loop input JSON object
    humanLoopInput = {
        'comprehendPredictions' : [],
        'labels': categories.split(','),
        'rowCount': 0,
        'bucketName': bucketName,
        'keyName': keyName
    }

    # split the body by period to get individual sentences
    for sentence in sentences:
        print(sentence)
        if len(sentence.strip()) > 0:
            humanLoopInput['comprehendPredictions'].append(json.loads(sentence))
            rowCount+=1
           

    humanLoopInput['rowCount'] = rowCount
    
    humanLoopName = 'Comprehend-Text' + str(int(round(time.time() * 1000)))
    print('Starting human loop - ' + humanLoopName)
    response = a2i.start_human_loop(
                                HumanLoopName=humanLoopName,
                                FlowDefinitionArn= flowDefnARN,
                                HumanLoopInput={
                                    'InputContent': json.dumps(humanLoopInput)
                                    }
                                )
    

    print('Success')
    return 0
