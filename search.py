from elasticsearch import Elasticsearch 
import json
import flask
from flask import request,render_template
import re
import sys
import numpy as np
import pickle 
from Models import Models

search = flask.Flask(__name__)
search.config["DEBUG"] = True

#ELASTICSEARCH_HOST="localhost"
ELASTICSEARCH_HOST="172.31.7.122"

es=Elasticsearch([{'host': ELASTICSEARCH_HOST, 'port': 9200}])
es.info

if es.ping():
  print('Connected to Elasticsearch')
else:
  print('Could not connect to elasticsearch')
  sys.exit()

def remove_special_chars(text):
  '''This function removes the special chars from the text'''
  text=str(text)
  text = re.sub('[^A-Za-z0-9]+', ' ', text)
  text=text.lower()
  return text
 
model=Models()

def get_query_doc(query):
  query=remove_special_chars(query)
  query_vector =model.get_tfidf_w2v(query)
  query_doc = {
    "query" : 
    {
            "script_score" :
            {
                "query" : {
                    "match_all": {}
                },
                "script" : {
                    "source": "cosineSimilarity(params.query_vector, 'text_vector') + 1.0",
                        "params": {"query_vector": query_vector}
                }
            }
    }
  }
  return query_doc


@search.route('/',  methods =["GET", "POST"])
@search.route('/search',  methods =["GET", "POST"])
def home():
  if request.method=='POST':
    query_doc=get_query_doc(request.form.get("search"))
    res= es.search(index='fashion',body=query_doc)
    image_ids=[]
    image_paths=[]
    for hit in res['hits']['hits']:
      image_ids.append(str(hit['_source']['imageid'])+".jpg")
      image_paths.append("https://flaskappfashion.s3.amazonaws.com/"+str(hit['_source']['imageid'])+".jpg")
    return render_template('search.html', image_name=image_paths,flag=True)
  else:
    return render_template("search.html",flag=False)
    
if __name__ == "__main__": 
  search.run(host ='0.0.0.0', port = 5000, debug = True)