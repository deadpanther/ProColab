import json
import boto3
import datetime;
import subprocess
import requests
# from requests_aws4auth import AWS4Auth

def lambda_handler(event, context):
    print(event)
    try:
        #print(event)
        title = event['title']
        content = event['content']
        timestamp = str(datetime.datetime.now())
        print(timestamp)
        accessToken = event['access_token']
        print(accessToken)
        client = boto3.client('cognito-idp', region_name='us-east-1')
        # response = client.get_user(
        # AccessToken=accessToken
        # )
        #print(response)
        loggedInEmail = ''
        userid=""
        userName=""
        print("1")
        # for attr in response['UserAttributes']:
        #     if attr['Name']== 'sub':
        #         userid= attr['Value']
        #     if attr['Name'] == 'email':
        #         loggedInEmail = attr['Value']
        #     if attr['Name']== 'given_name':
        #         userName= attr['Value']
        #print(loggedInEmail)
        comments=[]
        likes=""
        document={
            "userid":userid,
            "userName" :userName,
            "loggedInEmail": loggedInEmail,
            "Thread_Title": title,
            "Thread_content": content,
            "timestamp": timestamp,
            "comments":comments,
            "likes": likes
        }
        print(document)
        host = 'https://search-test-25gxq7rqzhndqmtzbzhorkg2fy.us-east-1.es.amazonaws.com'
        index = 'test'
        type = 'lambda-type'
        id= userid+timestamp
        url = host + '/' + index + '/' + type +'/'+ id
        service = 'es'
        region = 'us-east-1'
        headers = { "Content-Type": "application/json" }
        # credentials = boto3.Session().get_credentials()
        # awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)
        format = {"userid":userid,
            "userName" :userName,
            "loggedInEmail": loggedInEmail,
            "Thread_Title": title,
            "Thread_content": content,
            "timestamp": timestamp,
            "comments":comments,
            "likes": likes}

        response = requests.post(url, data=json.dumps(format).encode("utf-8"), headers=headers,auth=('admin', 'Admin@123'))
        print(response)
        print("------------firing request-----------------")
        #response=requests.post(url, auth=awsauth, json=document, headers=headers)
        print("------------after post request-----------")
        print(response)
    except Exception as e:
        print("someerror")
        print(e)
        return{
            'statusCode': 200,
            'body': json.dumps("event did not come to lambda"),
            'headers':{ 'Access-Control-Allow-Origin' : '*' }
        }
        