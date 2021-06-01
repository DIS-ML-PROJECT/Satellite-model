from PIL import Image
import os
from os import listdir
from os.path import isfile, join
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

def _int64_feature(value):
  """Returns an int64_list from a bool / enum / int / uint."""
  return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))

def _bytes_feature(value):
  """Returns a bytes_list from a string / byte."""
  if isinstance(value, type(tf.constant(0))):
    value = value.numpy() # BytesList won't unpack a string from an EagerTensor.
  return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

def serialize_example(nparray,wealth,wealthpooled,wealthpooled5country,country,urbanrural,lon_coord,lat_coord,year):
  """
  Creates a tf.train.Example message ready to be written to a file.
  """
  # Create a dictionary mapping the feature name to the tf.train.Example-compatible
  # data type.
  feature = {
      #image (vorhanden)
      'nparray': _dtype_feature(nparray),
      #wealthindex (vorhanden)
      'wealth': _float_feature(wealth),
      #wealthpooled
      'wealthpooled': _float_feature(wealthpooled),
      #wealthpooled5country
      'wealthpooled5country': _float_feature(wealthpooled5country),
      #country of survey (vorhanden)
      'country': _bytes_feature(country),
      # "U" for Urban, "R" for rural (vorhanden)
      'urbanrural': _bytes_feature(urbanrural),
      # Longitude Coords of the Center of the image (vorhanden)
      'centerlon': _float_feature(lon_coord),
      # Latitude Coords of the Center of the image (vorhanden)
      'centerlat': _float_feature(lat_coord),
      # year of the survey (vorhanden)
      'year': _int64_feature(year)
  }
  # Create a Features message using tf.train.Example.
  example_proto = tf.train.Example(features=tf.train.Features(feature=feature))
  return example_proto.SerializeToString()

#
dirpath = 'D:/satellite/data/nightlight'
exportpath = 'D:/satellite/data/tfrecords/'

onlyfiles = [f for f in listdir(dirpath) if isfile(join(dirpath, f))]
onlyfiles = onlyfiles[:10]
csvpath = os.path.abspath(os.path.join(os.path.abspath(__file__),"../../dataResearch/firstSample.csv"))
df = pd.read_csv(csvpath)
for i in onlyfiles:
    imgfile = dirpath + "/" + i
    with open(imgfile,'rb') as f:
        image = Image.open(f)
        image.load()
        image = image.resize((1050, 1050))
        imagearray = np.array(image.getdata())
        #Normalizing
        normalizedimagearray = stats.zscore(imagearray)
        #Get additional Features from CSV-File
        labelname = i.replace(".tif","")
        wealth = float(df["wealth"].at[df.ID[df.ID == labelname].index[0]].replace(",","."))
        with tf.io.TFRecordWriter(exportpath + labelname + '.tfrec') as writer:
            example = serialize_example(nparray=normalizedimagearray,wealth=wealth)
            writer.write(example)
        f.close()
        image.close()
    print(str(onlyfiles.index(i)+1) + "/" + str(len(onlyfiles)))