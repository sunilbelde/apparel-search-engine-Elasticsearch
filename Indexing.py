#Importing the packages

import pandas as pd
import re
import numpy as np
from elasticsearch import Elasticsearch 
import json



#ELASTICSEARCH_HOST="localhost"
ELASTICSEARCH_HOST="YOUR ELASTICSEARCH HOST IP"

es=Elasticsearch([{'host': ELASTICSEARCH_HOST, 'port': 9200}]) # Connectigng to elasticsearch
es.info

if es.ping():
  print('Connected to Elasticsearch')
else:
  print('Could not connect to elasticsearch')
  sys.exit()
  
  
lst=[6043,6568,7398,7938,9025,10263,10426,10904,11372,11944,14111,14531,15075,29905,31624,33019,35747,35961,37769,38104,38274,38403,] # This lines were corrupted in the data file.
data=pd.read_csv('styles.csv',skiprows=lst)
train=data.drop(['gender','masterCategory','subCategory','articleType','baseColour','season','year','usage'],axis=1)

def remove_special_chars(text):
  '''This function removes the special chars from the text'''
  text=str(text)
  text = re.sub('[^A-Za-z0-9]+', ' ', text)
  text=text.lower()
  return text
train['productDisplayName']=train['productDisplayName'].apply(lambda text: remove_special_chars(text))


#Creating a Mapping template for the documents in the elasticsearch index
b = {"mappings": {
         "properties": {
               "productDisplayName": {
             "type": "text"
             },
           "imageid":{
               "type":"integer"
           },
               "text_vector": {
                "type": "dense_vector",
                "dims": 512
            }
         }
     }
   }

INDEX_NAME='YOUR INDEX NAME'

ret = es.indices.create(index=INDEX_NAME, ignore=400, body=b) #Creating a Index in Elasticsearch
print(json.dumps(ret,indent=4))


#Creating a model which has tensorflow Universal sentence encoder model
model=Models()

#For each row in data injesting imageid,text and its vector representation with imageid as document id.

for index,row in tqdm(train.iterrows()):
    imageid=row['id']
    print(imageid)
    text=row['productDisplayName']
    vec=model.get_vec_rep(text)
    doc={
        "productDisplayName":text,
        "imageid":imageid,
        "text_vector":vec
    }
    res = es.index(index=INDEX_NAME, id=imageid, body=doc)
