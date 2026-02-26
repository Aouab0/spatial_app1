import streamlit as st
import geemap.foliumap as geemap # Utilisation du backend Folium pour Streamlit
import ee
from processing import SpatialProcessor

# --- 0. Initialisation indispensable ---
try:
    ee.Initialize()
except Exception as e:
    # Si l'auth échoue en local, on peut proposer ee.Authenticate()
    st.error("Earth Engine n'est pas initialisé. Vérifiez vos identifiants.")

st.set_page_config(layout="wide")
st.title("My first GOATED portal 🚀")

# 1. Connexion au moteur métier
@st.cache_resource
def load_engine():
    return SpatialProcessor()

engine = load_engine()

# 2. Formulaire de saisie
with st.sidebar:
    st.header("Coordonnées")
    lat = st.number_input("Latitude", value=48.85, format="%.4f")
    lon = st.number_input("Longitude", value=2.35, format="%.4f")
    submit = st.button("Afficher la zone", type="primary")

# 3. Logique d'affichage
# On crée la carte systématiquement
m = geemap.Map(center=[lat, lon], zoom=12)

if submit:
    with st.spinner("Récupération de l'image depuis le Cloud..."):
        try:
            img = engine.get_satellite_image(lat, lon)
            
            # Paramètres d'affichage (Sentinel-2)
            vis_params = {
                'bands': ['B4', 'B3', 'B2'], 
                'min': 0, 
                'max': 3000,
                'gamma': 1.4
            }
            
            m.addLayer(img, vis_params, 'Sentinel-2 Image')
            st.success(f"Image chargée pour {lat}, {lon}")
        except Exception as e:
            st.error(f"Erreur lors de la récupération : {e}")

# Affichage final (toujours à la fin)
m.to_streamlit(height=600)