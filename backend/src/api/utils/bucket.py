# AWS SDK
import boto3
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

#Creating connection to s3 Client
s3 = boto3.client(
    's3', aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
)