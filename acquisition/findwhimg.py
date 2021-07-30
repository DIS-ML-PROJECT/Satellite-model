import numpy as np
from osgeo import gdal
import os
#INFO and WARNING messages are not printed
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
from os import listdir
from os.path import join
from numpy.core.defchararray import endswith, index
import time
import pandas as pd

#declare the Directory, where the Sentinel-pictures are
s2path = 'E:/sciebo/Sentinel'
#create a list out of all geotiff-image filenames
s2files = [f for f in listdir(s2path) if endswith(join(s2path, f),".tif")==True]
#to get an estimate of the time left, we create a list with all durations of the progresses
timelist = []
#namelist is the resulting list of names, which have a lot of white pixels
namelist = []
#iterate over the list of filenames
for i in s2files:
    start = time.time()
    #get the correct path for the sentinelfile
    s2file = s2path+"/"+i
    #open the file with gdal
    s2raster = gdal.Open(s2file)
    #get the necessary Bands of the image
    rband = s2raster.GetRasterBand(4)
    gband = s2raster.GetRasterBand(3)
    bband = s2raster.GetRasterBand(2)
    #create numpy arrays per band
    rband = rband.ReadAsArray()
    gband = gband.ReadAsArray()
    bband = bband.ReadAsArray()
    #resize and flatten the bands to be the same size as the output files in our TFRecord-files
    rband = np.resize(rband,(1050,1050)).flatten()
    gband = np.resize(bband,(1050,1050)).flatten()
    bband = np.resize(bband,(1050,1050)).flatten()
    #get all indices of the pixels which are white(the pixel has a value of 3000 or higher)
    rlist = np.argwhere(rband >= 3000).tolist()
    glist = np.argwhere(gband >= 3000).tolist()
    blist = np.argwhere(bband >= 3000).tolist()
    #create an indexlist with all the indices of the whitepixels
    indexlist = [item for sublist in rlist for item in sublist]
    indexlist.extend([item for sublist in glist for item in sublist])
    indexlist.extend([item for sublist in blist for item in sublist])
    #get the relative amount of white pixels in the image by dividing the unique indices by the amount of pixels in the image
    pwhite = len(list(set(indexlist)))/(1050*1050)
    #if more than 20% of the image are declared white, we append the processed filename to the output-list
    if pwhite > 0.2:
        name = i.replace('.tif','')
        namelist.append(name)
    end = time.time()
    timelist.append(end-start)
    print(str(s2files.index(i)+1) + "/" + str(len(s2files)),time.strftime('%H:%M:%S',time.gmtime(int(sum(timelist)/len(timelist)*(len(s2files)-s2files.index(i))))))
#read in the csv file with more information about the pictures
df = pd.read_csv(os.path.abspath(os.path.join(os.path.abspath(__file__),"../../dataResearch/firstSample.csv")))
#Only take the Rows which are needed for the output
df = df[['ID','LATNUM','LONGNUM']]
#only keep all rows, if the ID is in the namelist 
df = df[df['ID'].isin(namelist)]
#create a blacklist of all images with more than 20% white pixels and save it as a csv-file
df.to_csv('blacklist.csv')