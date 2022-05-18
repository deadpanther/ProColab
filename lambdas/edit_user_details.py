import os
import sys
import json
import boto3
import requests
# import subprocess
# from requests_aws4auth import AWS4Auth

awsRegion = 'us-east-1'
accessID = ' '
secretKey = '  '

dbObject = boto3.resource('dynamodb',region_name=awsRegion, aws_access_key_id=accessID, aws_secret_access_key=secretKey)
dbtable = dbObject.Table('UserData')

def lambda_handler(event, context):
    print("EVENT",event)
    print(type(event))
    # get email from event dictionary
    access_token = event['queryStringParameters']['access_token']
    address = event['queryStringParameters']['address']
    email = event['queryStringParameters']['email']
    headline = event['queryStringParameters']['headline']
    experience = event['queryStringParameters']['experience']
    name = event['queryStringParameters']['name']
    phone = event['queryStringParameters']['phone']
    skills = event['queryStringParameters']['skills']
    
    
    print(email, access_token, address, experience, name, phone, skills)
    try:
        
        region = 'us-east-1'
        headers = { "Content-Type": "application/json" }
        credentials = boto3.Session().get_credentials()
        # user_details = dbtable.get_item(Key={'email': event['queryStringParameters']['email']})
        # print(user_details)
        res = dbtable.update_item(
        Key={
            'email': event['queryStringParameters']['email'],
        },
        AttributeUpdates={
            'name': {
                'Value': {name},
                'Action': 'PUT'
            },
            'address': {
                'Value': {address},
                'Action': 'PUT'
            },
            'experience': {
                'Value': {experience},
                'Action': 'PUT'
            },
            'phone': {
                'Value': {phone},
                'Action': 'PUT'
            },
            'headline': {
                'Value': {headline},
                'Action': 'PUT'
            },
            'skills': {
                'Value': {skills},
                'Action': 'PUT'
            },
            'access_token': {
                'Value': {access_token},
                'Action': 'PUT'
            },
        },
        ReturnValues="UPDATED_NEW"
    )
        valx = {
            "status": "updated"
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
        print("NO PROFILE FOUND")