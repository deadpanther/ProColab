import json
import boto3
import os
import sys
import subprocess
import requests
# from requests_aws4auth import AWS4Auth
from elasticsearch import Elasticsearch, RequestsHttpConnection

def lambda_handler(event, context):
    print(event)
    try:
        print("1")
        host = 'https://search-test-25gxq7rqzhndqmtzbzhorkg2fy.us-east-1.es.amazonaws.com/test/_search'
        # service = 'es'
        # region = 'us-east-1'
        # url = host + '/' + index + '/' + type
        headers = { "Content-Type": "application/json" }
        response = requests.get(host,headers={"Content-Type": "application/json"},auth=('admin', 'Admin@123')).json()
        print(response)
        thread_list=[]
        print(response['hits']['hits'])
        for item in response['hits']['hits']:
            if item['_source'].get('userid') is None:
                continue
            
            document={
                "userid": item['_source']['userid'],
                "userName" :item['_source']['userName'],
                "loggedInEmail": item['_source']['loggedInEmail'],
                "Thread_Title": item['_source']['Thread_Title'],
                "Thread_content": item['_source']['Thread_content'],
                "timestamp": item['_source']['timestamp'],
                "comments":item['_source']['comments'],
                "likes": item['_source']['likes']
            }
            thread_list.append(document)
        print("1")
        # print("sdflk",json.dumps((thread_list))
        valx = json.dumps(thread_list)
        return {
            'statusCode': 200,
            'body': valx,
            'headers':{ 'Access-Control-Allow-Origin' : '*' }
        }
    except Exception as e:
        print(e)
        return{
            'statusCode': 200,
            'body': json.dumps("event did not come to lambda"),
            'headers':{ 'Access-Control-Allow-Origin' : '*' }
        }