from PIL import Image
from os import listdir
from os.path import isfile, join

dirpath = 'D:/satellite/data/nightlight'
exportpath = 'D:/satellite/data/nightlightrightres/'

onlyfiles = [f for f in listdir(dirpath) if isfile(join(dirpath, f))]
for i in onlyfiles:
    imgfile = dirpath + "/" + i
    with open(imgfile,'rb') as f:
        image = Image.open(f)
        image = image.resize((1100, 1100))
        image.save(exportpath + i)
    print(onlyfiles.index(i))