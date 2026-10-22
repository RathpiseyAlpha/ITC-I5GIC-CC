import json
import boto3

def lambda_handler(event, context):
    s3_client = boto3.client('s3')
    
    bucket_name = '<BUCKET_NAME>'
    file_name = 'index.html'
    
    response = s3_client.get_object(Bucket=bucket_name, Key=file_name)
    data = response['Body'].read().decode('utf')

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/html',
        },
        'body': data
    }