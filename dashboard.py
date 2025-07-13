import streamlit as st
import folium
from streamlit_folium import st_folium
from folium import PolyLine
from geopy.distance import geodesic
import pandas as pd

# ------------------- Data ----------------------
corridor_data = {
    "Ambala to Jalandhar": {
        "Dera Bassi Site": {
            "station": {"lat": 30.5445, "lon": 76.8215},
            "substation": {"lat": 30.5488, "lon": 76.8260},
            "solar": {"lat": 30.5502, "lon": 76.8185}
        },
        "Kurukshetra Site": {
            "station": {"lat": 29.9679, "lon": 76.8783},
            "substation": {"lat": 29.9459, "lon": 76.8994},
            "solar": {"lat": 29.9500, "lon": 76.8500}
        },
        "Uchana Site": {
            "station": {"lat": 29.7450, "lon": 76.9726},
            "substation": {"lat": 29.7300, "lon": 76.9800},
            "solar": {"lat": 29.7350, "lon": 76.9600}
        }
    }
}

# ------------------- Sidebar Legend ----------------------
st.sidebar.title("🗺️ Legend")
st.sidebar.markdown("""
- 🔵 **Selected Station**
- 🔴 **Substation**
- 🟠 **Renewable Site**
- 📏 **Distance Lines**
""")

# ------------------- Header ----------------------
st.title("🚚 EV Corridor Dashboard")

# ------------------- Corridor and Station Selection ----------------------
selected_corridor = st.selectbox("Select EV Corridor", list(corridor_data.keys()))
station_names = list(corridor_data[selected_corridor].keys())
selected_site = st.selectbox("Select Station", station_names)

# ------------------- Extract Site Data ----------------------
site_data = corridor_data[selected_corridor][selected_site]
station = site_data["station"]
substation = site_data["substation"]
solar = site_data["solar"]

# ------------------- Distance Calculation ----------------------
distance_to_substation = round(geodesic(
    (station["lat"], station["lon"]),
    (substation["lat"], substation["lon"])
).km, 2)

distance_to_solar = round(geodesic(
    (station["lat"], station["lon"]),
    (solar["lat"], solar["lon"])
).km, 2)

# ------------------- Map ----------------------
m = folium.Map(location=[station["lat"], station["lon"]], zoom_start=13)

# Markers
folium.Marker(
    location=[station["lat"], station["lon"]],
    popup=f"{selected_site} - Station",
    icon=folium.Icon(color="blue", icon="info-sign")
).add_to(m)

folium.Marker(
    location=[substation["lat"], substation["lon"]],
    popup=f"{selected_site} - Substation",
    icon=folium.Icon(color="red", icon="flash")
).add_to(m)

folium.Marker(
    location=[solar["lat"], solar["lon"]],
    popup=f"{selected_site} - Solar Site",
    icon=folium.Icon(color="orange", icon="star")
).add_to(m)

# Connection Lines with distance tooltips
PolyLine(
    [(station["lat"], station["lon"]), (substation["lat"], substation["lon"])],
    color="black",
    weight=2.5,
    tooltip=f"Distance to Substation: {distance_to_substation} km"
).add_to(m)

PolyLine(
    [(station["lat"], station["lon"]), (solar["lat"], solar["lon"])],
    color="green",
    weight=2.5,
    tooltip=f"Distance to Solar Site: {distance_to_solar} km"
).add_to(m)

st_folium(m, width=700, height=500)

# ------------------- CSV DOWNLOAD ----------------------

df = pd.DataFrame([
    {
        "Corridor": selected_corridor,
        "Station": selected_site,
        "Station_Lat": station["lat"],
        "Station_Lon": station["lon"],
        "Substation_Lat": substation["lat"],
        "Substation_Lon": substation["lon"],
        "Solar_Lat": solar["lat"],
        "Solar_Lon": solar["lon"],
        "Distance to Substation (km)": distance_to_substation,
        "Distance to Solar Site (km)": distance_to_solar
    }
])

csv = df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Download Corridor Data as CSV",
    data=csv,
    file_name=f"{selected_corridor.replace(' ', '_')}_data.csv",
    mime='text/csv'
)
