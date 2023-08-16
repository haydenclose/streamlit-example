from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import os
"""
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""

st.title("fudge you streamlit")
in_csv = os.path.join(os.getcwd(), "data/Wreck Database_V2.4.csv")
wrecks = pd.read_csv(in_csv)
wreck_names = wrecks["Wreck_ID"].values.tolist()
wreck_name = st.selectbox("Select a wreck:", wreck_names, index = 2)
lat = pd.to_numeric(wrecks.loc[wrecks['Wreck_ID'] == wreck_name]['Latitude'])               # Get the latitude of selected wreck
lon = pd.to_numeric(wrecks.loc[wrecks['Wreck_ID'] == wreck_name]['Longitude'])                             # Get the longitude of selected wreck
S1Thresh = st.slider("S1 Threshold:", -30.0, -15.0,(-30.0,-23.5))
S2Thresh = st.slider("S2 threshold:", 1500, 7000,(2350,3000))

Sat_options = ['SENTINEL-1','SENTINEL-2', 'BOTH']
Satellite_selection = st.radio("Select an Satellite:", Sat_options, index = 2)

Orbit_options = ['ASCENDING','DESCENDING','BOTH']
Orbit_selection = st.radio("Select an orbit:", Sat_options, index = 2)

max_cloud_cover = st.slider("Max cloud %:", 0, 1000,100,1)
Dilation = st.slider("Pixel Dilation factor:", 0, 20,3,1)
PixelFilter = st.slider("Remove polygons smaller than:", 0, 1000,250,1)

def Next_button():
    st.write(" Next Button clicked!")

if st.button("Next image"):
    Next_button()

def my_function():
    st.write(" Previous Button clicked!")

if st.button("Next image"):
    Previous_button()





