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

s2path = 'E:/sciebo/Sentinel'
s2files = [f for f in listdir(s2path) if endswith(join(s2path, f),".tif")==True]
timelist = []
namelist = []
for i in s2files:
    start = time.time()
    s2file = s2path+"/"+i
    s2raster = gdal.Open(s2file)
    rband = s2raster.GetRasterBand(4)
    gband = s2raster.GetRasterBand(3)
    bband = s2raster.GetRasterBand(2)
    rband = rband.ReadAsArray()
    gband = gband.ReadAsArray()
    bband = bband.ReadAsArray()
    rband = np.resize(rband,(1050,1050)).flatten()
    gband = np.resize(bband,(1050,1050)).flatten()
    bband = np.resize(bband,(1050,1050)).flatten()
    rlist = np.argwhere(rband >= 3000).tolist()
    glist = np.argwhere(gband >= 3000).tolist()
    blist = np.argwhere(bband >= 3000).tolist()
    indexlist = [item for sublist in rlist for item in sublist]
    indexlist.extend([item for sublist in glist for item in sublist])
    indexlist.extend([item for sublist in blist for item in sublist])
    pwhite = len(list(set(indexlist)))/(1050*1050)
    if pwhite > 0.1:
        name = i.replace('.tif','')
        namelist.append(name)
    end = time.time()
    timelist.append(end-start)
    print(str(s2files.index(i)+1) + "/" + str(len(s2files)),time.strftime('%H:%M:%S',time.gmtime(int(sum(timelist)/len(timelist)*(len(s2files)-s2files.index(i))))))
    df = pd.read_csv(os.path.abspath(os.path.join(os.path.abspath(__file__),"../../dataResearch/firstSample.csv")))
    df = df[['ID','LATNUM','LONGNUM']]
    df = df[~df['ID'].isin(namelist)]
    df.to_csv('blacklist.csv')