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
    access_token = event['queryStringParameters']['access_token']
    address = event['queryStringParameters']['address']
    email = event['queryStringParameters']['email']
    experience = event['queryStringParameters']['experience']
    mobile = event['queryStringParameters']['mobile']
    name = event['queryStringParameters']['name']
    phone = event['queryStringParameters']['phone']
    skills = event['queryStringParameters']['skills']

    
    print(email)
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
            'mobile': {
                'Value': {mobile},
                'Action': 'PUT'
            },
            'phone': {
                'Value': {phone},
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
        print(res)
    except:

        print("Error:", sys.exc_info()[0])
        print("NO PROFILE FOUND")