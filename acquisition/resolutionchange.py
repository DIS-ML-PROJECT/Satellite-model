from PIL import Image
from os import listdir
from os.path import isfile, join

dirpath = 'C:/Users/esser/sciebo/Data_Acquisition/nightlight'

onlyfiles = [f for f in listdir(dirpath) if isfile(join(dirpath, f))]
for i in onlyfiles:
    imgfile = dirpath + "/" + i
    image = Image.open(imgfile)
    image = image.resize((1100, 1100))
    image.save(imgfile)
    print(onlyfiles.index(i))