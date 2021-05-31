from PIL import Image
import os
from os import listdir
from os.path import isfile, join
import copy
import pandas as pd
import numpy as np
import tensorflow as tf
#import tensorflow.io as tfio

dirpath = 'D:/satellite/data/nightlight'
exportpath = 'D:/satellite/data/nightlightrightres/'

onlyfiles = [f for f in listdir(dirpath) if isfile(join(dirpath, f))]
onlyfiles = onlyfiles[:1]
KEEP = []
KEEP_NAMES = []
for i in onlyfiles:
    imgfile = dirpath + "/" + i
    with open(imgfile,'rb') as f:
        image = Image.open(f)
        image.load()
        image = image.resize((1100, 1100))
        keep = copy.deepcopy(image)
        KEEP.append(keep)
        KEEP_NAMES.append(i)
        f.close()
        image.close()
        keep.close()
    print(onlyfiles.index(i))
csvpath = os.path.abspath(os.path.join(os.path.abspath(__file__),"../../dataResearch/firstSample.csv"))
df = pd.read_csv(csvpath)
for x,i in zip(KEEP,KEEP_NAMES):
    labelname = i.replace(".tif","")
    n = float(df["wealth"].at[df.ID[df.ID == labelname].index[0]].replace(",","."))
    print(x.show())
        #image_array = np.array(y.getdata())
        #print(image_array)
    #array = tf.keras.preprocessing.image.img_to_array(image_array)
    #tftensor  = tf.keras.preprocessing.image.img_to_array(image_array)
    #tfio.experimental.image.decode_tiff(image)