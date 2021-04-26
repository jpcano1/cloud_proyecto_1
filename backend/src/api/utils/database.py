from dotenv import load_dotenv, find_dotenv
import os
import boto3

load_dotenv(find_dotenv())
db = boto3.resource('dynamodb', region_name="us-east-1", aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                  aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"))
