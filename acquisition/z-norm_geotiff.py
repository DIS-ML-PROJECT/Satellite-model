# Load geotiff images from folder, z-normalize them, and save as numpy array in new folder

# imports
import numpy as np
import os
import rasterio
import scipy.stats as stats



for filename in os.listdir('/home/ripperflo/Downloads/nightlight_geotiffs'):
    if filename.endswith('.tif'):           # take TIFF-files only
        with rasterio.open(os.path.join('/home/ripperflo/Downloads/nightlight_geotiffs', filename)) as f:   # open GeoTiff and store in f
            img = f.read()          # open GeoTiff as 3D numpy array
            matrix = img[0]         # 3D array to 2D array because nighlight images has only one band
            z_norm = stats.zscore(matrix)           # normalize 2D array
            np.save('/home/ripperflo/Downloads/nightlight_z-arrays/{}.npy'.format(filename[:-4]), z_norm)   # save to npy file


