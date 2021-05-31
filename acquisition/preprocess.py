from PIL import Image
import os
from os import listdir
from os.path import isfile, join
import copy
import pandas as pd
import numpy as np
import tensorflow as tf
import scipy.stats as stats

# SELFMADE AND IN TESTING

def _dtype_feature(ndarray):
        """match appropriate tf.train.Feature class with dtype of ndarray. """
        assert isinstance(ndarray, np.ndarray)
        dtype_ = ndarray.dtype
        if dtype_ == np.float64 or dtype_ == np.float32:
            return tf.train.Feature(float_list=tf.train.FloatList(value=ndarray))
        elif dtype_ == np.int64:
            return tf.train.Feature(int64_list=tf.train.Int64List(value=ndarray))
        else:  
            raise ValueError("The input should be numpy ndarray. \
                               Instead got {}".format(ndarray.dtype))
# from Tensorflow doc

def _float_feature(value):
  """Returns a float_list from a float / double."""
  return tf.train.Feature(float_list=tf.train.FloatList(value=[value]))

def serialize_example(nparray,label):
  """
  Creates a tf.train.Example message ready to be written to a file.
  """
  # Create a dictionary mapping the feature name to the tf.train.Example-compatible
  # data type.
  feature = {
      'nparray': _dtype_feature(nparray),
      'label': _float_feature(label),
  }
  # Create a Features message using tf.train.Example.
  example_proto = tf.train.Example(features=tf.train.Features(feature=feature))
  return example_proto.SerializeToString()

#
dirpath = 'D:/satellite/data/nightlight'
exportpath = 'D:/satellite/data/tfrecords/'

onlyfiles = [f for f in listdir(dirpath) if isfile(join(dirpath, f))]
csvpath = os.path.abspath(os.path.join(os.path.abspath(__file__),"../../dataResearch/firstSample.csv"))
df = pd.read_csv(csvpath)
for i in onlyfiles:
    imgfile = dirpath + "/" + i
    with open(imgfile,'rb') as f:
        image = Image.open(f)
        image.load()
        image = image.resize((1100, 1100))
        imagearray = np.array(image.getdata())
        #Normalizing
        normalizedimagearray = stats.zscore(imagearray)
        imagearray = normalizedimagearray
        labelname = i.replace(".tif","")
        n = float(df["wealth"].at[df.ID[df.ID == labelname].index[0]].replace(",","."))
        with tf.io.TFRecordWriter(exportpath + labelname + '.tfrec') as writer:
            example = serialize_example(nparray=imagearray,label=n)
            writer.write(example)
        f.close()
        image.close()
    print(str(onlyfiles.index(i)+1) + "/" + str(len(onlyfiles)))
