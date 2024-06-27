import streamlit as st
import numpy as np
import pandas as pd
import folium
from streamlit_folium import folium_static
import pickle
from folium.plugins import HeatMap
from PIL import Image

import pandas as pd

df = pd.read_csv('https://data.nasa.gov/api/views/gh4g-9sfh/rows.csv?accessType=DOWNLOAD')
df.dropna(inplace=True)

st.title("Predicción de Caída de Meteoritos")


reclat = st.number_input("Ingrese la latitud:", min_value=-90.0, max_value=90.0, step=0.0001)
reclong = st.number_input("Ingrese la longitud:", min_value=-180.0, max_value=180.0, step=0.0001)


m = folium.Map(location=[reclat, reclong], zoom_start=20)


center_lat = df['reclat'].mean()
center_long = df['reclong'].mean()

data = df[['reclat', 'reclong']].values.tolist()
heat_map = folium.Map(location=[center_lat, center_long], zoom_start=15)

HeatMap(data).add_to(m)

if st.button("Predecir caída de meteorito"):
    
    
    file_path = '../Models/vecinos_default_42.sav'
    with open (file_path, 'rb') as file :
        vecinos_default_42 = pickle.load(file)
    features = np.array([[reclat, reclong]])
    prediction = vecinos_default_42.predict(features)[0]
    
    
    st.write(f"Predicción: {prediction}")

    
    folium.Marker([reclat, reclong], popup=f"Predicción: {prediction}").add_to(m)

    
    if "predictions" in st.session_state:
        HeatMap(st.session_state.predictions).add_to(m)


folium_static(m)