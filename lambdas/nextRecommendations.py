import json
import boto3
import os
import nltk
from nltk.tokenize import word_tokenize
import pandas as pd
nltk.data.path.append("/tmp")
nltk.download("punkt", download_dir="/tmp")
s3_client = boto3.client("s3")

def Sort_Tuple(tup): 
    tup.sort(key = lambda x: x[1]) 
    return tup
def merge(list1, list2):
      
    merged_list = [(list1[i], list2[i]) for i in range(0, len(list1))]
    return merged_list

def lambda_handler(event, context):
    # TODO implement
    obj = s3_client.get_object(Bucket = 'procolabtraindata',Key = "Final_clean_data.csv")
    techcrunch_data = pd.read_csv(obj['Body'],encoding='unicode_escape')

    emails = []
    similarity = []
    # X_list = word_tokenize(event['queryStringParameters']['user_skill'])
    X_list = event['queryStringParameters']['skills']
    X_set = set(X_list)
    for i in range(len(techcrunch_data)):
        
        Y_list = word_tokenize(techcrunch_data['Skills'][i])
        l1 =[]; l2=[]
    
        # remove stop words from the string   
        Y_set = set(Y_list)
    
        # form a set containing keywords of both strings 
        rvector = X_set.union(Y_set) 
        for w in rvector:
            if w in X_set: l1.append(1) # create a vector
            else: l1.append(0)
            if w in Y_set: l2.append(1)
            else: l2.append(0)
        c = 0
          
        # cosine formula 
        for i in range(len(rvector)):
                c+= l1[i]*l2[i]
        cosine = c / float((sum(l1)*sum(l2))**0.5)
        emails.append(techcrunch_data['Email'][i])
        similarity.append(cosine)
    tuple_full = list(zip(emails, similarity))
    tuple_full = Sort_Tuple(tuple_full)

    print(tuple_full)
    valx = {
        "Person1": tuple_full[-1][0],
        "Person2": tuple_full[-2][0],
        "Person3": tuple_full[-3][0],
        "Person4": tuple_full[-4][0],
        "Person5": tuple_full[-5][0],
        "Person6": tuple_full[-6][0],
        "Person7": tuple_full[-7][0],
        "Person8": tuple_full[-8][0],
        "Person9": tuple_full[-9][0],
        "Person10": tuple_full[-10][0],
    }

    val = {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin':'*'},
        'body': json.dumps(valx),
        'isBase64Encoded': False
    }
    print(val)
    return val
    
    return {
        'statusCode': 200,
        'body': json.dumps(val)
    }