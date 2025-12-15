# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal.
"""

# -*- coding: utf-8 -*-
"""
Simulador Ovocitos ⇄ Embriones
Equipo Juana Crespo
"""

import streamlit as st
import pandas as pd

# --------------------------------------------------
# CONFIGURACIÓN DE LA PÁGINA
# --------------------------------------------------
st.set_page_config(
    page_title="Simulador Ovocitos ⇄ Embriones | Equipo Juana Crespo",
    page_icon="🩺",
    layout="centered",
)

COLOR_PRINCIPAL = "#C2A27B"
COLOR_TEXTO = "#C2A27B"
COLOR_FONDO = "#3d4752"

# --------------------------------------------------
# ESTILOS
# --------------------------------------------------
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


st.markdown(f"""
<style>
/* Color de texto global */
html, body, [class*="st-"], .stApp {{
    color: {COLOR_TEXTO} !important;
}}

/* Labels de inputs y opciones */
label, .stRadio > label, .stSelectbox > label, .stNumberInput label {{
    color: {COLOR_TEXTO} !important;
}}

/* Texto de las opciones dentro de radio y selectbox */
div[data-testid="stMarkdownContainer"], div[role="radiogroup"] p, div[role="listbox"] div {{
    color: {COLOR_TEXTO} !important;
}}

/* Encabezados generados con st.markdown o st.write */
h1, h2, h3, h4, h5, h6, p, span {{
    color: {COLOR_TEXTO} !important;
}}

/* Texto de los inputs numéricos */
input[type="number"], input[type="text"] {{
    color: {COLOR_TEXTO} !important;
    background-color: {COLOR_FONDO} !important;
    border: 1px solid {COLOR_TEXTO}33;
}}

/* Ajuste del color de los botones (+ / -) */
button[kind="secondary"] > div > p {{
    color: {COLOR_TEXTO} !important;
}}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>Simulador Ovocitos ⇄ Embriones</div>", unsafe_allow_html=True)

# --------------------------------------------------
# DATOS
# --------------------------------------------------
data = {
    "Edad": ["Hasta 34", 35, 36, 37, 38, 39, 40, 41, 42, 43, "44 o más"],

    "% MII/Ovocitos Obtenidos": [
        0.792127592454, 0.784349078582, 0.801761569493, 0.787576148805,
        0.802363889512, 0.800015794848, 0.791417245299, 0.792935524757,
        0.783993411191, 0.803992981979, 0.796405743839
    ],

    "% Fecundados 2PN/Ovocitos Obtenidos": [
        0.653285596938012, 0.64270944534009, 0.660446181582556,
        0.648414601861447, 0.644156544525678, 0.643432710178685,
        0.632198033145782, 0.632239099682429, 0.621672225256302,
        0.630365597769279, 0.609795507441275
    ],

    "% Embriones Útiles/Fecundados 2PN": [
        0.560909624901375, 0.569103316567104, 0.56432524845238,
        0.56619615565783, 0.554778853880855, 0.548645346385857,
        0.508918198112147, 0.484464015944833, 0.41948483355831,
        0.366563039511128, 0.294096303023395
    ],

    "Embriones Transferibles/Embriones Útiles": [
        0.64, 0.57, 0.56, 0.52, 0.45, 0.40, 0.34, 0.26, 0.21, 0.14, 0.07
    ]
}

df = pd.DataFrame(data)

# --------------------------------------------------
# CONTROLES
# --------------------------------------------------
modo = st.radio(
    "Selecciona el modo de simulación:",
    ["De ovocitos a embriones", "De embriones a ovocitos"]
)

edad = st.selectbox("Selecciona la edad de la paciente:", df["Edad"])
fila = df[df["Edad"] == edad].iloc[0]

# --------------------------------------------------
# MODO 1: OVOCITOS → EMBRIONES
# --------------------------------------------------
if modo == "De ovocitos a embriones":

    ovocitos = st.number_input(
        "Introduce el número de ovocitos recuperados:",
        min_value=1, value=10, step=1
    )

    mii = ovocitos * fila["% MII/Ovocitos Obtenidos"]
    fecundados = ovocitos * fila["% Fecundados 2PN/Ovocitos Obtenidos"]
    utiles = fecundados * fila["% Embriones Útiles/Fecundados 2PN"]
    transferibles = utiles * fila["Embriones Transferibles/Embriones Útiles"]

    st.markdown(f"### Resultados estimados para {ovocitos} ovocitos recuperados:")
    st.write(f"**Ovocitos MII:** {mii:.1f}")
    st.write(f"**Fecundados (2PN):** {fecundados:.1f}")
    st.write(f"**Embriones útiles:** {utiles:.1f}")
    st.write(f"**Embriones transferibles:** {transferibles:.1f}")

# --------------------------------------------------
# MODO 2: EMBRIONES → OVOCITOS
# --------------------------------------------------
else:
    tipo_objetivo = st.radio(
        "Selecciona el tipo de objetivo:",
        ["Embriones útiles", "Embriones transferibles"]
    )

    if tipo_objetivo == "Embriones transferibles":
        transferibles_deseados = st.number_input(
            "Introduce el número de embriones transferibles deseados:",
            min_value=1, value=2, step=1
        )

        utiles_necesarios = transferibles_deseados / fila["Embriones Transferibles/Embriones Útiles"]
        fecundados_necesarios = utiles_necesarios / fila["% Embriones Útiles/Fecundados 2PN"]
        ovocitos_necesarios = fecundados_necesarios / fila["% Fecundados 2PN/Ovocitos Obtenidos"]
        mii_necesarios = ovocitos_necesarios * fila["% MII/Ovocitos Obtenidos"]

        st.markdown(f"### Estimación para obtener {transferibles_deseados} embriones transferibles:")
        st.write(f"**Ovocitos recuperados necesarios:** {ovocitos_necesarios:.1f}")
        st.write(f"**Ovocitos MII estimados:** {mii_necesarios:.1f}")
        st.write(f"**Fecundados (2PN) necesarios:** {fecundados_necesarios:.1f}")
        st.write(f"**Embriones útiles necesarios:** {utiles_necesarios:.1f}")

    else:
        utiles_deseados = st.number_input(
            "Introduce el número de embriones útiles deseados:",
            min_value=1, value=3, step=1
        )

        fecundados_necesarios = utiles_deseados / fila["% Embriones Útiles/Fecundados 2PN"]
        ovocitos_necesarios = fecundados_necesarios / fila["% Fecundados 2PN/Ovocitos Obtenidos"]
        mii_necesarios = ovocitos_necesarios * fila["% MII/Ovocitos Obtenidos"]
        transferibles_estimados = utiles_deseados * fila["Embriones Transferibles/Embriones Útiles"]

        st.markdown(f"### Estimación para obtener {utiles_deseados} embriones útiles:")
        st.write(f"**Ovocitos recuperados necesarios:** {ovocitos_necesarios:.1f}")
        st.write(f"**Ovocitos MII estimados:** {mii_necesarios:.1f}")
        st.write(f"**Fecundados (2PN) necesarios:** {fecundados_necesarios:.1f}")
        st.write(f"**Embriones transferibles estimados:** {transferibles_estimados:.1f}")

# --------------------------------------------------
# NOTA FINAL
# --------------------------------------------------
st.markdown(
    "<div class='note'>Estimaciones basadas en probabilidades históricas; "
    "los resultados individuales pueden variar.</div>",
    unsafe_allow_html=True
)
