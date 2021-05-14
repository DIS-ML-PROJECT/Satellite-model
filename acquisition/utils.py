from typing import Tuple
from datetime import date
import ee
import pandas as pd

def surveyyear_to_range(year: int,satellitename: str) -> Tuple[str, str]:
    if satellitename == "S2":
        if 2012<=year<=2015:
            start_date = '2015-06-24'
            end_date = '2016-01-01'
        elif year == 2016:
            start_date = '2016-01-01'
            end_date = '2017-01-01'
        elif year == 2017:
            start_date = '2017-01-01'
            end_date = '2018-01-01'
        elif year == 2018:
            start_date = '2018-01-01'
            end_date = '2019-01-01'
        elif year == 2019:
            start_date = '2019-01-01'
            end_date = '2020-01-01'
        elif year == 2020:
            start_date = '2020-01-01'
            end_date = '2021-01-01'
        elif year == 2021:
            start_date = '2021-01-01'
            end_date = date.today().strftime('%Y-%m-%d')
        else:
            raise ValueError(f'Jahr wird nicht unterstützt: {year}. '
                            'Alle Jahre vor 2012 werden nicht beachtet.')
    elif satellitename == "nl":
        if year == 2012:
            start_date = '2012-01-01'
            end_date = '2013-01-01'
        elif year == 2013:
            start_date = '2013-01-01'
            end_date = '2014-01-01'
        elif year == 2014:
            start_date = '2014-01-01'
            end_date = '2015-01-01'
        elif year == 2015:
            start_date = '2015-01-01'
            end_date = '2016-01-01'
        elif year == 2016:
            start_date = '2016-01-01'
            end_date = '2017-01-01'
        elif year == 2017:
            start_date = '2017-01-01'
            end_date = '2018-01-01'
        elif year == 2018:
            start_date = '2018-01-01'
            end_date = '2019-01-01'
        elif year == 2019:
            start_date = '2019-01-01'
            end_date = '2020-01-01'
        elif year == 2020:
            start_date = '2020-01-01'
            end_date = '2021-01-01'
        elif year == 2021:
            start_date = '2021-01-01'
            end_date = date.today().strftime('%Y-%m-%d')
        else:
            raise ValueError(f'Jahr wird nicht unterstützt: {year}. '
                            'Alle Jahre vor 2012 werden nicht beachtet.')
    return start_date, end_date

def df_to_fc(df: pd.DataFrame, lat_colname: str = 'LATNUM',
             lon_colname: str = 'LONGNUM') -> ee.FeatureCollection:
    '''
    Args
    - csv_path: str, path to CSV file that includes at least two columns for
        latitude and longitude coordinates
    - lat_colname: str, name of latitude column
    - lon_colname: str, name of longitude column
    Returns: ee.FeatureCollection, contains one feature per row in the CSV file
    '''
    # convert values to Python native types
    # see https://stackoverflow.com/a/47424340
    df = df.astype('object')

    ee_features = []
    for i in range(len(df)):
        props = df.iloc[i].to_dict()

        # oddly EE wants (lon, lat) instead of (lat, lon)
        _geometry = ee.Geometry.Point([
            props[lon_colname],
            props[lat_colname],
        ])
        ee_feat = ee.Feature(_geometry, props)
        ee_features.append(ee_feat)

    return ee.FeatureCollection(ee_features)