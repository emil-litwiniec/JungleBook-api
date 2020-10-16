import boto3
import os

AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

s3 = boto3.resource('s3',
                    aws_access_key_id=AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
                    )

bucket = s3.Bucket('jungle-book-storage')


def file_upload(filename, file):
    try:
        bucket.put_object(Key=filename, Body=file)
    except Exception as e:
        print(e)
        raise
