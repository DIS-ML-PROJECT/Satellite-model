from PIL import Image
import os
from os import listdir
from os.path import join
from numpy.core.defchararray import endswith
import pandas as pd
import numpy as np
import tensorflow as tf
import scipy.stats as stats
import io
from osgeo import gdal
import time

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

#CONSTANTS
nlpath = 'D:/sciebo/nightlight'
s2path = 'D:/sciebo/Sentinel'
exportpath = 'D:/satellite/data/tfrecords/'
##
def minmax():
    minmaxlist = []
    s2files = [f for f in listdir(s2path) if endswith(join(s2path, f),".tif")==True]
    for i in s2files:
        start = time.time()
        nlfile = nlpath + "/" + i
        s2file = s2path+"/"+i
        s2raster = gdal.Open(s2file) 
        for n in range(s2raster.RasterCount):
            f = n + 1
            s2band = s2raster.GetRasterBand(f)
            s2band = s2band.ReadAsArray()
            s2band = np.resize(s2band,(1050,1050))
            min = s2band.min()
            max = s2band.max()
            if len(minmaxlist) < s2raster.RasterCount + 1:
                s2minmax = [min,max]
                minmaxlist.append(s2minmax)
            elif min < minmaxlist[n][0]:
                minmaxlist[n][0] = min
            if max > minmaxlist[n][1]:
                minmaxlist[n][1] = max
        nlraster = gdal.Open(nlfile)
        nlband = nlraster.GetRasterBand(1)
        nlband = nlband.ReadAsArray()
        nlband = np.resize(nlband,(1050,1050))
        nlmin = nlband.min()
        nlmax = nlband.max()
        if len(minmaxlist) < s2raster.RasterCount + 1:
            nlminmax = [nlmin,nlmax]
            minmaxlist.append(nlminmax)
        elif nlmin < minmaxlist[16][0]:
            minmaxlist[16][0] = nlmin
        if nlmax > minmaxlist[16][1]:
            minmaxlist[16][1] = nlmax
        end = time.time()
        print(str(s2files.index(i)+1) + "/" + str(len(s2files)),"Time elapsed:",round(end - start,2),"sec")
    return minmaxlist

def preprocess():
  """[summary]
  """
  onlyfiles = [f for f in listdir(s2path) if endswith(join(s2path, f),".tif")]
  csvpath = os.path.abspath(os.path.join(os.path.abspath(__file__),"../../dataResearch/Data_with_Pooled.csv"))
  df = pd.read_csv(csvpath)
  minmaxlist = minmax()
  for i in onlyfiles:
      imgfile = s2path + "/" + i
      with open(imgfile,'rb') as f:
          image = Image.open(f)
          image.load()
          image = image.resize((1050, 1050))
          imagearray = np.array(image.getdata())
          #Normalized
          normalizedimagearray = (imagearray-min)/(max-min)
          #Get additional Features from CSV-File
          labelname = i.replace(".tif","")
          index = df.ID[df.ID == labelname].index
          wealthpooled = float(df['wealthpooled'].loc[index].max().replace(",","."))
          wealthpooled5country = float(df['wealthpooled5country'].loc[index].max().replace(",","."))
          country = bytes(df['country'].loc[index].max(), 'utf-8')
          urbanrural = bytes(df['URBAN_RURA'].loc[index].max(), 'utf-8')
          csvlat = float(df['LATNUM'].loc[index].max().replace(",","."))
          csvlon = float(df['LONGNUM'].loc[index].max().replace(",","."))
          year = int(df['year'].loc[index].max())
          wealth = float(df['wealth'].loc[index].max().replace(",","."))
          with tf.io.TFRecordWriter(exportpath + labelname + '.tfrec') as writer:
              example = serialize_example(nparray=normalizedimagearray,
                                          wealth=wealth,
                                          wealthpooled=wealthpooled,
                                          wealthpooled5country=wealthpooled5country,
                                          country=country,
                                          urbanrural=urbanrural,
                                          lon_coord=csvlon,
                                          lat_coord=csvlat,
                                          year=year)
              writer.write(example)
          f.close()
          image.close()
      print(str(onlyfiles.index(i)+1) + "/" + str(len(onlyfiles)))

minmax()