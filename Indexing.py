import pandas as pd
import re
import numpy as np
from elasticsearch import Elasticsearch 
import json
from sklearn.feature_extraction.text import TfidfVectorizer



#ELASTICSEARCH_HOST="localhost"
ELASTICSEARCH_HOST="172.31.7.122"

es=Elasticsearch([{'host': ELASTICSEARCH_HOST, 'port': 9200}])
es.info

if es.ping():
  print('Connected to Elasticsearch')
else:
  print('Could not connect to elasticsearch')
  sys.exit()
  
  
lst=[6043,6568,7398,7938,9025,10263,10426,10904,11372,11944,14111,14531,15075,29905,31624,33019,35747,35961,37769,38104,38274,38403,]
data=pd.read_csv('styles.csv',skiprows=lst)
train=data.drop(['gender','masterCategory','subCategory','articleType','baseColour','season','year','usage'],axis=1)

def remove_special_chars(text):
  '''This function removes the special chars from the text'''
  text=str(text)
  text = re.sub('[^A-Za-z0-9]+', ' ', text)
  text=text.lower()
  return text
train['productDisplayName']=train['productDisplayName'].apply(lambda text: remove_special_chars(text))

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
                "dims": 300
            }
         }
     }
   }
ret = es.indices.create(index='fashion', ignore=400, body=b) #400 caused by IndexAlreadyExistsException, 
print(json.dumps(ret,indent=4))

word_embeddings = dict()
glove_model = open('glove.6B.300d.txt', encoding="utf8")
for line in glove_model: # For each line in text file
  row = line.split() 
  word = row[0] # First word 
  vector = np.asarray(row[1:], dtype='float32') # Remaining text is 300 dimensional embeddings
  word_embeddings[word] = vector # Creating a dictionay with word as key and embeddings  vector as value
glove_model.close()

glove_words=word_embeddings.keys()

tfidf_model = TfidfVectorizer() 
tfidf_model.fit(train['productDisplayName'].values) # Fitting the tfidf vectorizer on train data
# we are converting a dictionary with word as a key, and the idf as a value
idf_dictionary = dict(zip(tfidf_model.get_feature_names(), list(tfidf_model.idf_)))
tfidf_words = set(tfidf_model.get_feature_names())

def get_tfidf_w2v(text):
    vector=np.zeros(300) #Intialising a 300-dim vector
    tf_idf_weight =0
    for word in text.split(): # For each word in vector
      if (word in glove_words) and (word in tfidf_words):
        vec=word_embeddings[word] #Getting the word's w2v representation
        tf_idf = idf_dictionary[word]*(text.count(word)/len(text.split())) # Calulating tfidf value of word using idf values
        vector += (vec * tf_idf) # Computing weighted sum of tfidf-w2v
        tf_idf_weight += tf_idf
    if tf_idf_weight!=0:
      vector/=tf_idf_weight # Averaging the weighted sum of tfidf-w2v
    return vector
    
from tqdm import tqdm
for index,row in tqdm(train.iterrows()):
    imageid=row['id']
    print(imageid)
    text=row['productDisplayName']
    vec=get_tfidf_w2v(text)
    doc={
        "productDisplayName":text,
        "imageid":imageid,
        "text_vector":vec
    }
    res = es.index(index="fashion", id=imageid, body=doc)