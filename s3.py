import boto3
import os 

client = boto3.client('s3', region_name='ap-south-1')

        
for file in os.listdir("static"):
  if file.endswith('.jpg'):
    print(file)
    client.upload_file('static/'+file, 'flaskappfashion', file, ExtraArgs={'ContentType': "image/jpeg", 'ACL': "public-read"})