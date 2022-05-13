import os
import sys
import json
import boto3
import requests 

endpoint_name = <INSERT_ENDPOINT_NAME>
runtime = boto3.Session().client(service_name='sagemaker-runtime',region_name='us-east-1')

response = runtime.invoke_endpoint(EndpointName=endpoint_name, ContentType='application/x-image', Body=payload)
print(response['Body'].read())
