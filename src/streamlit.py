import streamlit as st
import numpy as np
import pandas as pd
import folium
from pickle import load
from streamlit_folium import folium_static

model = load(open("../Models/.sav", "rb"))

st.title("Predicción de Caída de Meteoritos")

reglat = st.number_input("Ingrese la latitud:",
                         min_value=-90.0, max_value=90.0, step=0.0001)
reclong = st.number_input("Ingrese la longitud:",
                          min_value=-180.0, max_value=180.0, step=0.0001)

if st.button("Predecir caída de meteorito"):
    features = np.array([[reglat, reclong]])
    prediction = model.predict(features)[0]

    st.write(f"Predicción: {prediction}")

    geoprediction = folium.Map(location=[reglat, reclong], zoom_start=10)
    folium.Marker([reglat, reclong], popup=f"Predicción: {
                  prediction}").add_to(geoprediction)

    folium_static(geoprediction)
