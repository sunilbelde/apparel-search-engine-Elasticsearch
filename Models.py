import tensorflow as tf
tf.enable_eager_execution()
import tensorflow_hub as hub

class Models():
  def __init__(self):
    self.model=hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")
    
  def get_vec_rep(self,text):
    vector=tf.make_ndarray(tf.make_tensor_proto(self.model([text]))).tolist()[0]
    return vector