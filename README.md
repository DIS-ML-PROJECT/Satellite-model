# Satellite_model
# Main Tasks

## Constructing a Wealth Index from 43 DHS surveys (2009-2016 23 countries of Africa)
- Converting descriptions into scores (e.g. flooring type)
- creating weights on household level based on the first principle components
 -extract latitude and longitude coordinates from survey data (per cluster)
  - Cluster: - rural areas: one village
            - urban areas: one district
- remove clusters with invalid gps coordinates *(-> 19.669 Cluster)*

- validate wealth index by comparing to different measures (e.g. sum of all assets owned)

- add census data (including questions about wealth) (second-level administrative)
				- LSMS Daten 
					  - exclude migrant household
- aggregate all data on second-level administrative
- exclude variables that are not available in LSMS data (fridge, motorbike)
- *strong correlation to consum on village level*


## Satellite images (according to sustainlab-group)
- Export  Nightlight- und Daylight-Satellite images centeres on each cluster location (Landsat-Archive Google Earth Engine)
  - 3-year median composite (daylight images): 
    - 2009-11, 2012-14 und 2015-17
    - Sentinel II and Sentinel I (if these are available for these years)
  
        - *gather clear satellite images (no clouds,...)*
        - *no distortion due to short-time variations*
        - *wealth is developing rather slowly over time*

  -  3-year median composite (nightlight images)
		-2009-11 (DMSP27)
		-2012-14,2015-17 (VIIRS28)
		
- Nearest-Neighbor-Upsampling to cover the same geographic space

- Slicing satellite images to the input size of the CNN




