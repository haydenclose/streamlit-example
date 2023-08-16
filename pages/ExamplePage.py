from io import StringIO
import ee
from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import os
import leafmap.foliumap as leafmap
import folium.plugins as plugins
ee.Authenticate()
"""
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""

st.title("Oil Mapping")
in_csv = os.path.join(os.getcwd(), "data/Wreck Database_V2.4.csv")
wrecks = pd.read_csv(in_csv)
wreck_names = wrecks["Wreck_ID"].values.tolist()
wreck_name = st.sidebar.selectbox("Select a wreck:", wreck_names, index = 2)
lat = pd.to_numeric(wrecks.loc[wrecks['Wreck_ID'] == wreck_name]['Latitude'])               # Get the latitude of selected wreck
lon = pd.to_numeric(wrecks.loc[wrecks['Wreck_ID'] == wreck_name]['Longitude'])                             # Get the longitude of selected wreck
S1Thresh = st.sidebar.slider("S1 Threshold:", -30.0, -15.0,(-30.0,-23.5))
S2Thresh = st.sidebar.slider("S2 threshold:", 1500, 7000,(2350,3000))

Sat_options = ['SENTINEL-1','SENTINEL-2', 'BOTH']
Satellite_selection = st.sidebar.radio("Select an Satellite:", Sat_options, index = 2)

Orbit_options = ['ASCENDING','DESCENDING','BOTH']
Orbit_selection = st.sidebar.radio("Select an orbit:", Orbit_options, index = 2)

max_cloud_cover = st.sidebar.slider("Max cloud %:", 0, 1000,100,1)
Dilation = st.sidebar.slider("Pixel Dilation factor:", 0, 20,3,1)
PixelFilter = st.sidebar.slider("Remove polygons smaller than:", 0, 1000,250,1)
col1, col2 = st.columns(2)
def Next_button():
    st.write(" Next Button clicked!")

if col1.button("Next image"):
    Next_button()

def Previous_button():
    st.write(" Previous Button clicked!")

if col2.button("Previous image"):
    Previous_button()
StartDate   = '01-01-2014'
EndDate = '01-04-2016'
#measure = plugins.MeasureControl(position="bottomleft", active_color="orange")
#measure.add_to(m)

if Satellite_selection == 'SENTINEL-1' or Satellite_selection == 'BOTH':                               # If to see if create feature collection with S1 or both
    S1ImgCol = (ee.ImageCollection('COPERNICUS/S1_GRD').                                            # Selects the Sentinel 1 image collection
     filterDate(str(StartDate), str(EndDate)).                                         # Selects only the dates from time period chosen above
     filterMetadata('instrumentMode', 'equals', 'IW').                                             # Selects the instrument mode that we want
     filter(ee.Filter.eq('orbitProperties_pass', str(Orbit_selection))).                               # Selects the orbit path we want
     filterBounds(geom))                                                                           # Selects only images that our wreck is contained within
    S1ImgCol = S1ImgCol.map(add_S1_date)                                                            # Adds the image date to image metadata in easy way to read
    ImgCol_gammaMap = S1ImgCol.map(gammaMap)                                                        # Process the ImageCollection through the gammaMap algorithm
    ImgCol_gammaMap = ImgCol_gammaMap.map(add_S1Gamma_date)                                         # Gamma function removes alot of the metadata so add date back in

#if Satellite_selection == 'SENTINEL-2' or Satellite_selection == 'BOTH':                               # If to see if create feature collection with S2 or both
#   S2ImgCol = (ee.ImageCollection('COPERNICUS/S2_HARMONIZED').                                       # Selects the Sentinel 2 image collection
#     filterDate(str(StartDate), str(EndDate)).                                          # Selects only the dates from time period chosen above
#     filterBounds(geom).                                                                            # Selects only images that our wreck is contained within
#     filterMetadata('CLOUDY_PIXEL_PERCENTAGE', 'less_than', max_cloud_cover))                 # Filter image collection by cloud cover
#   S2ImgCol = S2ImgCol.map(add_S2_date)                                                              # Add the image date to the metadata in an easy way to read

#if Satellite_selection == 'BOTH':                                                                    # If both S1 and S2 combine collections
#   ImageCol = S1ImgCol.merge(S2ImgCol)                                                              # Merge ImageCollections, note raw S1
#   ImageCol = ImageCol.sort("Date")                                                                 # Order images by Date
#   ImgList = ee.ImageCollection(ImageCol).toList(99999)                                             # Creates a list of the images to select from
#   ImageColGM = ImgCol_gammaMap.merge(S2ImgCol)                                                     # Merge ImageCollections, note gammaS1
#   ImageColGM = ImageColGM.sort("Date")                                                             # Order images by Date
#   ImgListGM = ee.ImageCollection(ImageColGM).toList(99999)                                         # Creates a list of the d images to select from
#elif Satellite_selection == 'SENTINEL-1':                                                            # Create collections based just on S1
 #  ImageCol = S1ImgCol                                                                              # ImageCollection = S1
#   ImgListGM = ee.ImageCollection(ImgCol_gammaMap).toList(99999)                                    # Creates a list of the gammacorrected images to select from
#elif  Satellite_selection == 'SENTINEL-2':                                                           # Create collections based just on S2
 #    ImageCol = S2ImgCol                                                                            # ImageCollection = S2
#ImgList = ee.ImageCollection(ImageCol).toList(99999)                                               # Creates a list of the images to select from
#Datatable = pd.DataFrame(columns = ['Wreck_Name', 'Date', 'Oil_Area_m2','Low_Threshold','High_Threshold', 'Satellite','Comment'])# Empty dataframe for polygon oil spill area
m = leafmap.Map(
    center=[float(lat), float(lon)],
    zoom=int(10),
    locate_control=True,
    draw_control=True,
    measure_control=False,
)


# MultiMap = geemap.Map()                                                                            # Base map
# MultiMap.centerObject(geom, 10)                                                                    # Center the map on the wreck
m.add_points_from_xy(wrecks, x="Longitude", y="Latitude")                                   # Add wreck locations
#m = 0                                                                                              # Number to assign polygon number
#n = 0                                                                                              # Used to add or subtract to change the image
#img = ee.Image(ee.List(ImgList).get(n))                                                            # Get the image from the image list to display the first image
#if ee.Image(img).getString('Satellite').getInfo()  == 'SENTINEL-1A' or ee.Image(img).getString('Satellite').getInfo()  == 'SENTINEL-1B': # If S1 use below parmaeters
#  img = ee.Image(ee.List(ImgList).get(n)).select('VV')                                              # Selects the VV band
#  img_params = {'bands':'VV', 'min':-25, 'max':5}                                                   # Display setting for the VV band
#else: img_params = {'min': 0,'max': 3000,'bands': ['B4','B3','B2']}                                # Otherwise select the RGB bands
 #IMgdate = img.date()                                                                               # Get the acquisition date of the image
 #date_string = IMgdate.format('YYYY-MM-dd').getInfo()                                               # Format the date as a string
#m.addLayer(img, img_params, 'Satellite Image',True)                                         # Add the image to the map
m.to_streamlit(height=600)

