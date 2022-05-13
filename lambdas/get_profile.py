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
        email = user_details.get('Item').get('email')

        try:
            name = list(user_details.get('Item').get('name'))
        except:
            name = 'None'
        try:
            address = list(user_details.get('Item').get('address'))
        except:
            address = 'None'
        try:
            experience = list(user_details.get('Item').get('experience'))
        except:
            experience = 'None'
        try:
            mobile = list(user_details.get('Item').get('mobile'))
        except:
            mobile = 'None'
        try:
            phone = list(user_details.get('Item').get('phone'))
        except:
            phone = 'None'
        try:
            skills = list(user_details.get('Item').get('skills'))
        except:
            skills = 'None'
        try:
            access_token = list(user_details.get('Item').get('access_token'))
        except:
            access_token = ''
        print(name)
        print(address)
        print(experience)
        print(mobile)
        print(phone)
        print(skills)
        print(access_token)
        print(email)
        valx = {
                "email" : email,
                "name" : name,
                "address" : address,
                "experience" : experience,
                "mobile" : mobile,
                "phone" : phone,
                "skills" : skills,
                "access_token" : access_token,
            }
        
        val = {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin':'*'},
            'body': json.dumps(valx),
            'isBase64Encoded': False
        }
        print(val)
        return val
    except:
        print("Error:", sys.exc_info()[0])