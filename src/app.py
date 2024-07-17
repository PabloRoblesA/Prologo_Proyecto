#Atajo de apertura de visualizacion en Streamlit
# Link de app por Render: https://starsafe-0-1.onrender.com/
import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import folium_static
import pickle
from folium.plugins import HeatMap
from PIL import Image

@st.cache_data
def cargar_datos(url):
    data = pd.read_csv(url)
    data.dropna(inplace=True)
    return data

df = cargar_datos('https://data.nasa.gov/api/views/gh4g-9sfh/rows.csv?accessType=DOWNLOAD')

@st.cache_resource
def cargar_modelo(file_path):
    with open(file_path, 'rb') as file:
        modelo = pickle.load(file)
    return modelo

import base64
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(jpg_file):
    bin_str = get_base64_of_bin_file(jpg_file)
    page_bg_img = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{bin_str}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)
set_background('Image_App.jpg')

vecinos_default_42 = cargar_modelo('../Models/vecinos_default_42.sav')

st.title("Predicción de Caída de Meteoritos")

reclat = st.number_input("Ingrese la latitud:", min_value=-90.0, max_value=90.0, step=0.0001)
reclong = st.number_input("Ingrese la longitud:", min_value=-180.0, max_value=180.0, step=0.0001)

center_lat = df['reclat'].mean()
center_long = df['reclong'].mean()
m = folium.Map(location=[center_lat, center_long], zoom_start=4)

data = df[['reclat', 'reclong']].values.tolist()
HeatMap(data).add_to(m)

if st.button("Predecir caída de meteorito"):
    features = np.array([[reclat, reclong]])
    prediction = vecinos_default_42.predict(features)[0]
    st.write(f"Predicción: {prediction}")


m = folium.Map(location=[reclat, reclong], zoom_start=7)
folium.Marker([reclat, reclong], popup=f"Predicción: {prediction}").add_to(m)
HeatMap(data).add_to(m)

folium_static(m)

st.title("Mapa de Calor de Predicción de Caída de Meteoritos")

uploaded_file = st.file_uploader("Nasa_MeteoriteLanding", type="csv")
if uploaded_file is not None:
    df_uploaded = pd.read_csv(uploaded_file)
    if 'reclat' in df_uploaded.columns and 'reclong' in df_uploaded.columns:
        coordinates = df_uploaded[['reclat', 'reclong']].values.tolist()
        m_uploaded = folium.Map(location=[0, 0], zoom_start=4)
        HeatMap(coordinates).add_to(m_uploaded)
        folium_static(m_uploaded)
    else:
        st.error("El archivo CSV debe contener columnas 'reclat' y 'reclong'.")
else:
    st.info("Por favor, carga un archivo CSV para visualizar el mapa de calor.")