import ee
import pandas as pd
import utils
import os


# Trigger the authentication flow.
#ee.Authenticate()
# Initialize the library.
ee.Initialize()

#Path of CSV-File with columns ID,year,LATITUDE,LONGITUDE
csvpath = '../dataResearch/firstSample.csv'
#name all column names
#year
year = 'year'
#Latitude and Longitude Coordinates
LATNUM = 'LATNUM'
LONGNUM= 'LONGNUM'
#ID for Filenames
surveyid = 'ID'
#Export parameters
DHS_EXPORT_FOLDER = 'geotiff_raw'
# image export parameters
PROJECTION = 'EPSG:3857'  # see https://epsg.io/3857
#1100 pixel times 10m equals 11000mx11000m image
SCALE = 10                # export resolution: 10m/px
IMAGE_DIMENSION = 5500  #radius of the wanted image in m

#create a Dataframe to iterate over and get all neccessary information
df = pd.read_csv(csvpath)
df = df[df.year >= 2012]
df = df[:10]
for i in range(len(df)):
    #get all constants out of the Dataframe
    start_date,end_date = utils.surveyyear_to_range(df[year].iloc[i],satellitename='S2')
    lat = float(df[LATNUM].iloc[i].replace(',', '.'))
    lon = float(df[LONGNUM].iloc[i].replace(',', '.'))
    name = df[surveyid].iloc[i]
    print(name,lon,lat)
    # Define the geometry of the area for which you would like images.
    aoi = ee.Geometry.Point(lon,lat)
    geom = ee.Geometry.Polygon(utils.point_to_box_coords(aoi=aoi,dimensionradius=IMAGE_DIMENSION))
    #create the neccessary Image Collections
    s2 = ee.ImageCollection('COPERNICUS/S2')
    criteria = ee.Filter.date(start_date,end_date)
    s2 = s2.filter(criteria).filterBounds(geom).median()
    task_config = {
        'region': geom.coordinates().getInfo(),
        'folder': DHS_EXPORT_FOLDER,
        'scale': 10,
        'crs': PROJECTION,
        'description': name
    }

    # Export Image
    task = ee.batch.Export.image.toDrive(s2, **task_config)
    task.start()