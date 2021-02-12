import pickle
import numpy as np

class Models():
  def __init__(self):
    self.tfidf_model=pickle.load( open( "tfidf.pkl", "rb" ) )
    self.word_embeddings=pickle.load( open( "embeddings.pkl", "rb" ) )
    self.glove_words=self.word_embeddings.keys()
    self.idf_dictionary = dict(zip(self.tfidf_model.get_feature_names(), list(self.tfidf_model.idf_)))
    self.tfidf_words = set(self.tfidf_model.get_feature_names())
    
  def get_tfidf_w2v(self,text):
    vector=np.zeros(300) #Intialising a 300-dim vector
    tf_idf_weight =0
    for word in text.split(): # For each word in vector
      if (word in self.glove_words) and (word in self.tfidf_words):
        vec=self.word_embeddings[word] #Getting the word's w2v representation
        tf_idf = self.idf_dictionary[word]*(text.count(word)/len(text.split())) # Calulating tfidf value of word using idf values
        vector += (vec * tf_idf) # Computing weighted sum of tfidf-w2v
        tf_idf_weight += tf_idf
    if tf_idf_weight!=0:
      vector/=tf_idf_weight # Averaging the weighted sum of tfidf-w2v
    return vector