import json
import base64
import boto3
def lambda_handler(event, context):
    # TODO implement
    print(event)
    data = event['img']
    # customlabel = event['customlabels']
    loginemail = event['email']
    print(data)
    name = event['name']
    client = boto3.client('cognito-idp', region_name='us-east-1')
    # response = client.get_user(
    # AccessToken=token
    # )
    # print(response)
    name1=name
    access_token=event['access_token']
    # for attr in response['UserAttributes']:
    #     if attr['Name'] == 'sub':
    #         userid= attr['Value']
    #     if attr['Name'] == 'given_name':
    #         name1= attr['Value']
    #     if attr['Name']== 'email':
    #         logInEmail= attr['Value']
    filename=name1
    s3_resource = boto3.resource('s3')
    obj = s3_resource.Object(bucket_name='resumeparserdata', key=filename)
    pdf = base64.b64decode(data, validate=True)
    # our S# Bucket
    s3 = boto3.client('s3')
    bucket = 'resumeparserdata'
    path = '/tmp/'+name
    filename=name1
    handler = open(path, "wb+")
    handler.write(pdf)
    handler.close()
        # upload the temp image to s3
    s3.upload_file(path, bucket, filename, ExtraArgs={'Metadata': {'name': name1, 'logInEmail': loginemail, 'access_token': access_token}})
    return {
        'statusCode': 200,
        'body': json.dumps('Image uploaded successfully')
    }