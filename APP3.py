# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import streamlit as st
import pandas as pd

st.set_page_config(
page_title="Simulador Ovocitos ⇄ Embriones | Equipo Juana Crespo",
page_icon="👶",
layout="centered",
)

COLOR_PRINCIPAL = "#C2A27B" # beige Juana Crespo
COLOR_TEXTO = "#C2A27B"
COLOR_FONDO = "#3d4752"

st.markdown(f"""
<style>
body {{
background-color: {COLOR_FONDO};
color: {COLOR_TEXTO};
}}
.stApp {{
background-color: {COLOR_FONDO};
}}
.title {{
text-align: center;
color: {COLOR_TEXTO};
font-size: 36px;
font-weight: bold;
}}
.note {{
color: {COLOR_PRINCIPAL};
font-size: 13px;
text-align: center;
margin-top: 20px;
}}
.stSlider > div, .stRadio > label, .stSelectbox label {{
color: {COLOR_TEXTO};
}}
</style>
""", unsafe_allow_html=True)



st.markdown("<div class='title'>Simulador Ovocitos ⇄ Embriones</div>", unsafe_allow_html=True)

data = {
"Edad": ["Hasta 34", 35, 36, 37, 38, 39, 40, 41, 42, 43, "44 o más"],
"% Fecundados 2PN/Ovocitos Obtenidos": [0.65, 0.64, 0.66, 0.65, 0.64, 0.64, 0.63, 0.63, 0.62, 0.63, 0.61],
"% Embriones Útiles/Fecundados 2PN": [0.56, 0.57, 0.56, 0.57, 0.55, 0.55, 0.51, 0.48, 0.42, 0.37, 0.29],
"Embriones Transferibles/Embriones Útiles": [0.64, 0.57, 0.56, 0.52, 0.45, 0.40, 0.34, 0.26, 0.21, 0.14, 0.07]
}

df = pd.DataFrame(data)


modo = st.radio(
"Selecciona el modo de simulación:",
["De ovocitos a embriones", "De embriones a ovocitos"]
)

edad = st.selectbox("Selecciona la edad de la paciente:", df["Edad"])
fila = df[df["Edad"] == edad].iloc[0]


if modo == "De ovocitos a embriones":
    ovocitos = st.number_input("Introduce el número de ovocitos obtenidos:", min_value=1, value=10, step=1)
    fecundados = ovocitos * fila["% Fecundados 2PN/Ovocitos Obtenidos"]
    utiles = fecundados * fila["% Embriones Útiles/Fecundados 2PN"]
    transferibles = utiles * fila["Embriones Transferibles/Embriones Útiles"]

    st.markdown(f"### Resultados estimados para {ovocitos} ovocitos:")
    st.write(f"**Fecundados (2PN):** {fecundados:.1f}")
    st.write(f"**Embriones útiles:** {utiles:.1f}")
    st.write(f"**Embriones transferibles:** {transferibles:.1f}")
    
else:
    tipo_objetivo = st.radio(
    "Selecciona el tipo de objetivo:",
    ["Embriones transferibles", "Embriones útiles"]
    )
    if tipo_objetivo == "Embriones transferibles":
        transferibles_deseados = st.number_input("Introduce el número de embriones transferibles deseados:", min_value=1, value=2, step=1)
        
        utiles_necesarios = transferibles_deseados / fila["Embriones Transferibles/Embriones Útiles"]
        fecundados_necesarios = utiles_necesarios / fila["% Embriones Útiles/Fecundados 2PN"]
        ovocitos_necesarios = fecundados_necesarios / fila["% Fecundados 2PN/Ovocitos Obtenidos"]
        
        st.markdown(f"### Estimación para obtener {transferibles_deseados} embriones transferibles:")
        st.write(f"**Embriones útiles necesarios:** {utiles_necesarios:.1f}")
        st.write(f"**Fecundados (2PN) necesarios:** {fecundados_necesarios:.1f}")
        st.write(f"**Ovocitos necesarios:** {ovocitos_necesarios:.1f}")

    else:
        utiles_deseados = st.number_input("Introduce el número de embriones útiles deseados:", min_value=1, value=3, step=1)
        
        fecundados_necesarios = utiles_deseados / fila["% Embriones Útiles/Fecundados 2PN"]
        ovocitos_necesarios = fecundados_necesarios / fila["% Fecundados 2PN/Ovocitos Obtenidos"]
        transferibles_estimados = utiles_deseados * fila["Embriones Transferibles/Embriones Útiles"]
        
        st.markdown(f"### Estimación para obtener {utiles_deseados} embriones útiles:")
        st.write(f"**Fecundados (2PN) necesarios:** {fecundados_necesarios:.1f}")
        st.write(f"**Ovocitos necesarios:** {ovocitos_necesarios:.1f}")
        st.write(f"**Embriones transferibles estimados:** {transferibles_estimados:.1f}")
        
        
st.markdown("<div class='note'>Estimaciones basadas en probabilidades históricas; resultados individuales pueden variar.</div>", unsafe_allow_html=True)