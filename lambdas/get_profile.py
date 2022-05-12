import os
import sys
import json
import boto3
import requests 
# import subprocess
# from requests_aws4auth import AWS4Auth

awsRegion = 'us-east-1'
accessID = 'AKIA5HYBIAG5IXDQEBPC'
secretKey = '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'

dbObject = boto3.resource('dynamodb',region_name=awsRegion, aws_access_key_id=accessID, aws_secret_access_key=secretKey)
dbtable = dbObject.Table('UserData')

def lambda_handler(event, context):
    print("EVENT",event)
    print(type(event))
    # get email from event dictionary
    email = event['queryStringParameters']['email']
    
    print(email)
    try:
        
        region = 'us-east-1'
        headers = { "Content-Type": "application/json" }
        credentials = boto3.Session().get_credentials()
        user_details = dbtable.get_item(Key={'email': event['queryStringParameters']['email']})
        print(user_details)
        
        val = user_details.get('Item').get('Name')
        print(type(val))
        json_object = {
            "email" : user_details.get('Item').get('email')
        }
        print(json_object)
        val = {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin':'*'},
            'body': json.dumps({
                'email': user_details.get('Item').get('email'),
                # 'Name': "neel"
            }),
            'isBase64Encoded': False
        }
        print(val)
        return val
    except:
        print("Error:", sys.exc_info()[0])