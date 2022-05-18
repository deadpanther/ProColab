import json
import boto3
import datetime
import os
import sys
import subprocess
os.system('pip3 install requests -t /tmp/ --no-cache-dir')
sys.path.insert(1, '/tmp/')
os.system('pip3 install requests_aws4auth -t /tmp/ --no-cache-dir')
sys.path.insert(1, '/tmp/')
import requests
from requests_aws4auth import AWS4Auth

def lambda_handler(event, context):
    print("event:",event)
    try:
        print("1")
        l = event['body']
        ld = json.loads(l)
        print("data:",ld)
        print(ld['like'])
        like= ld['like']
        print(like)
        userid= ld['userid']
        print(userid)
        timestampCreated= ld['timestampCreated']
        indexid= userid+timestampCreated
        print("2")
        host = 'https://search-test-25gxq7rqzhndqmtzbzhorkg2fy.us-east-1.es.amazonaws.com'
        index = 'test'
        type = 'lambda-type'
        id= indexid
        url = host + '/' + index + '/' + type +'/'+ id
        service = 'es'
        region = 'us-east-1'
        headers = { "Content-Type": "application/json" }
        print("30")
        #host = 'https://search-test-25gxq7rqzhndqmtzbzhorkg2fy.us-east-1.es.amazonaws.com/test/_search'
        headers = { "Content-Type": "application/json" }
        response = requests.get(url,headers={"Content-Type": "application/json"},auth=('admin', 'Admin@123')).json()
        print("res:",response)
        print("k:",response['_source']['likes'])
        ly= response['_source']['likes']
        print("k:",ly)
        if ly=="":
            ly=str(like)
        else:
            ly= str(int(l)+like)
        print("kupdated:",ly)
        print("51")
        document={
            "userid":response['_source']['userid'],
            "userName" :response['_source']['userName'],
            "loggedInEmail": response['_source']['loggedInEmail'],
            "Thread_Title": response['_source']['Thread_Title'],
            "Thread_content": response['_source']['Thread_content'],
            "timestamp": response['_source']['timestamp'],
            "comments": response['_source']['comments'],
            "likes": ly
        }
        print("docs;",document)
        # format = {"userid":res['_source']['userid'],
        #     "userName" :res['_source']['userName'],
        #     "loggedInEmail": res['_source']['loggedInEmail'],
        #     "Thread_Title": res['_source']['Thread_Title'],
        #     "Thread_content": res['_source']['Thread_content'],
        #     "timestamp": res['_source']['timestamp'],
        #     "comments": res['_source']['comments'],
        #     "likes": l}
        response = requests.post(url, data=json.dumps(document).encode("utf-8"), headers=headers,auth=('admin', 'Admin@123'))
        #response=requests.post(url, auth=awsauth, json=document, headers=headers)
        print(response.content)
    except Exception as e:
        print("somerror")
        print(e)
        return{
            'statusCode': 200,
            'body': json.dumps("event did not come to lambda"),
            'headers':{ 'Access-Control-Allow-Origin' : '*' }
        }