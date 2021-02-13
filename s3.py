import boto3
import os 


#Connecting aws S3 
#Note: You need to pass AWS ACCESS KEY and PASSWORD from aws cli or mention in your enironment variables

client = boto3.client('s3', region_name='ap-south-1')

BUCKET_NAME='YOUR-BUCKET-NAME'       
for file in os.listdir("static"):
  if file.endswith('.jpg'):
    print(file)
    client.upload_file('static/'+file, BUCKET_NAME , file, ExtraArgs={'ContentType': "image/jpeg", 'ACL': "public-read"}) # Uploading files to BUCKET
