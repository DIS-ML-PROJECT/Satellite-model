#! /usr/bin/env python
#Import necessary Libraries
import os
#INFO and WARNING messages are not printed
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
from os import listdir
from os.path import join
from numpy.core.defchararray import endswith
import pandas as pd
import numpy as np
import tensorflow as tf
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

def serialize_example(B1,B2,B3,B4,B5,B6,B7,B8,B8A,B9,B10,B11,B12,NL,wealth,wealthpooled,wealthpooled5country,country,urbanrural,lon_coord,lat_coord,year):
  """
  Creates a tf.train.Example message ready to be written to a file.
  """
  # Create a dictionary mapping the feature name to the tf.train.Example-compatible data type.
  feature = {
      #Band 1: Aerosols
      'Band 1': _dtype_feature(B1),
      #Band 2: Blue
      'Band 2': _dtype_feature(B2),
      #Band 3: Green
      'Band 3': _dtype_feature(B3),
      #Band 4: Green
      'Band 4': _dtype_feature(B4),
      #Band 5: Red Edge 1
      'Band 5': _dtype_feature(B5),
      #Band 6: Red Edge 2
      'Band 6': _dtype_feature(B6),
      #Band 7: Red Edge 3
      'Band 7': _dtype_feature(B7),
      #Band 8: NIR
      'Band 8': _dtype_feature(B8),
      #Band 8A: Red Edge 4
      'Band 8A': _dtype_feature(B8A),
      #Band 9: Water Vapor
      'Band 9': _dtype_feature(B9),
      #Band 10: Cirrus
      'Band 10': _dtype_feature(B10),
      #Band 11: SWIR 1 
      'Band 11': _dtype_feature(B11),
      #Band 12: SWIR 2
      'Band 12': _dtype_feature(B12),
      #Nightlight Band
      'Nightlight Band': _dtype_feature(NL),
      #wealthindex
      'wealth': _float_feature(wealth),
      #wealthpooled
      'wealthpooled': _float_feature(wealthpooled),
      #wealthpooled5country
      'wealthpooled5country': _float_feature(wealthpooled5country),
      #country of survey
      'country': _bytes_feature(country),
      # "U" for Urban, "R" for rural
      'urbanrural': _bytes_feature(urbanrural),
      # Longitude Coords of the Center of the image
      'centerlon': _float_feature(lon_coord),
      # Latitude Coords of the Center of the image
      'centerlat': _float_feature(lat_coord),
      # year of the survey
      'year': _int64_feature(year)
  }
  # Create a Features message using tf.train.Example.
  example_proto = tf.train.Example(features=tf.train.Features(feature=feature))
  return example_proto.SerializeToString()

#CONSTANTS
nlpath = 'E:/sciebo/nightlight'
s2path = 'E:/sciebo/Sentinel'
exportpath = 'E:/sciebo/tfrecords'
##
def minmax():
    """creates a list of all min and max values per band

    Returns:
        List[List]: Returns a list of lists in which are the min and max values of the bands
    """
    minmaxlist = []
    timelist = []
    #create a list of the filenames of all sentinel-images
    s2files = [f for f in listdir(s2path) if endswith(join(s2path, f),".tif")==True]
    print("STEP 1/2")
    print("EXPORTING MIN AND MAX VALUES PER BAND")
    for i in s2files:
        start = time.time()
        nlfile = nlpath + "/" + i
        s2file = s2path+"/"+i
        #open the file
        s2raster = gdal.Open(s2file) 
        #iterate over the bands of each image
        for n in range(s2raster.RasterCount):
            f = n + 1
            s2band = s2raster.GetRasterBand(f)
            #read the pixels of the band as an numpy-array
            s2band = s2band.ReadAsArray()
            #resize the bands to have all images in the same size
            s2band = np.resize(s2band,(1050,1050))
            #get the min and max values of each band to be able to 0-1 normalize after
            min = s2band.min()
            max = s2band.max()
            #check if there are already values for the band
            if len(minmaxlist) < s2raster.RasterCount + 1:
                s2minmax = [min,max]
                minmaxlist.append(s2minmax)
            # if the min value of the open band is smaller than the saved minimal value, overwrite it
            if min < minmaxlist[n][0]:
                minmaxlist[n][0] = min
            #if the max value of the open band is higher than the saves maximum value, overwrite it
            if max > minmaxlist[n][1]:
                minmaxlist[n][1] = max
        #open the nightlight img
        nlraster = gdal.Open(nlfile)
        nlband = nlraster.GetRasterBand(1)
        #read the only band of the image as a numpy-array
        nlband = nlband.ReadAsArray()
        #resize it the same way as the sentinel images
        nlband = np.resize(nlband,(1050,1050))
        #get the min and max values of the band
        nlmin = nlband.min()
        nlmax = nlband.max()
        #check if there are already information about min and max values for the nightlight images
        if len(minmaxlist) < s2raster.RasterCount + 1:
            nlminmax = [nlmin,nlmax]
            minmaxlist.append(nlminmax)
        #if the min value of the open nightlight image is smaller than the saved minimal value, overwrite it
        if nlmin < minmaxlist[16][0]:
            minmaxlist[16][0] = nlmin
        #if the max value of the open nightlight image is higher than the saves maximum value, overwrite it
        if nlmax > minmaxlist[16][1]:
            minmaxlist[16][1] = nlmax
        end = time.time()
        timelist.append(end-start)
        print("Step 1/2",str(s2files.index(i)+1) + "/" + str(len(s2files)),"Est. time left:",time.strftime('%H:%M:%S',time.gmtime(int(sum(timelist)/len(timelist)*(len(s2files)-s2files.index(i))))))
        #throw out the Quality Bands (QA10,QA20,QA60)
        minmaxlist = [i for j,i in enumerate(minmaxlist) if j not in [13,14,15]]
    return minmaxlist

def preprocess():
    """
    Gather information about the images and then write it into a TFRecords file for easier use in the Training Model

    Outut: TFRecord-Files per Image with all Bands of the image,
    the nightlight band,
    the different information about the wealth of the cluster,
    the country,
    the information wether the cluster is considered urban or rural,
    the geocoordinates
    and the year
    """
    #get a list of all sentinel-image filenames
    s2files = [f for f in listdir(s2path) if endswith(join(s2path, f),".tif")==True]
    #read in a csv-file with information about the cluster
    csvpath = os.path.abspath(os.path.join(os.path.abspath(__file__),"../../dataResearch/Data_with_Pooled.csv"))
    df = pd.read_csv(csvpath)
    #get the min and max values per band 
    minmaxlist = minmax()
    timelist = []
    print("STEP 2/2")
    print("CREATING TFRECORDS")
    for i in s2files:
        start = time.time()
        s2file = s2path + "/" + i
        #Get Features out of the Dataframe
        #get the name of the label (equals the SurveyID in the data)
        labelname = i.replace(".tif","")
        #get the index of the entry to get the information out of the dataframe
        index = df.ID[df.ID == labelname].index
        wealthpooled = float(df['wealthpooled'].loc[index].max().replace(",","."))
        wealthpooled5country = float(df['wealthpooled5country'].loc[index].max().replace(",","."))
        country = bytes(df['country'].loc[index].max(), 'utf-8')
        urbanrural = bytes(df['URBAN_RURA'].loc[index].max(), 'utf-8')
        csvlat = float(df['LATNUM'].loc[index].max().replace(",","."))
        csvlon = float(df['LONGNUM'].loc[index].max().replace(",","."))
        year = int(df['year'].loc[index].max())
        wealth = float(df['wealth'].loc[index].max().replace(",","."))
        #Get all Bands out of the GEOTIFF File
        s2raster = gdal.Open(s2file)
        bandlist = []
        for n in range(s2raster.RasterCount):
            f = n+1
            if n not in [13,14,15]:
                s2band = s2raster.GetRasterBand(f)
                s2band = s2band.ReadAsArray()
                s2band = np.resize(s2band,(1050,1050)).flatten()
                min = minmaxlist[n][0]
                max = minmaxlist[n][1]
                s2band = (s2band-min)/(max-min)
                bandlist.append(s2band.flatten())
        #get the Nightlight Band out of the GEOTIFF File
        nlfile = nlpath + "/" + i
        nlraster = gdal.Open(nlfile)
        nlband = nlraster.GetRasterBand(1)
        nlband = nlband.ReadAsArray()
        nlband = np.resize(nlband,(1050,1050)).flatten()
        min = minmaxlist[13][0]
        max = minmaxlist[13][1]
        nlband = (nlband-min)/(max-min)
        bandlist.append(nlband)
        #create a TFRecords-File with the TFRecordWriter
        with tf.io.TFRecordWriter(exportpath + '/' + labelname + '.tfrec') as writer:
            example = serialize_example(B1=bandlist[0],
                                        B2=bandlist[1],
                                        B3=bandlist[2],
                                        B4=bandlist[3],
                                        B5=bandlist[4],
                                        B6=bandlist[5],
                                        B7=bandlist[6],
                                        B8=bandlist[7],
                                        B8A=bandlist[8],
                                        B9=bandlist[9],
                                        B10=bandlist[10],
                                        B11=bandlist[11],
                                        B12=bandlist[12],
                                        NL=bandlist[13],
                                        wealth=wealth,
                                        wealthpooled=wealthpooled,
                                        wealthpooled5country=wealthpooled5country,
                                        country=country,
                                        urbanrural=urbanrural,
                                        lon_coord=csvlon,
                                        lat_coord=csvlat,
                                        year=year)
            writer.write(example)
        end = time.time()
        timelist.append(end-start)
        print("Done!",str(s2files.index(i)+1) + "/" + str(len(s2files)),"Est. time left:",time.strftime('%d:%H:%M:%S',time.gmtime(int(sum(timelist)/len(timelist)*(len(s2files)-s2files.index(i))))))

if __name__ == '__main__':
    preprocess()
