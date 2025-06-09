from django.shortcuts import render
import folium
from folium import Icon
import pandas as pd
from django.conf import settings
import os

def index(request):
    # Leer data de AguasEjemplo.csv
    csv_path = os.path.join(settings.BASE_DIR, "data", "AguasEjemplo.csv")
    df = pd.read_csv(csv_path)

    # Crear mapa base
    m = folium.Map(
        location=[-33.45, -70.67], # Coordenadas de Santiago, Chile
        zoom_start=5,
        tiles="CartoDB.Positron",
        attr="© OpenStreetMap, © CartoDB",
        width="100%"
    )

    # Añadir los Markers de los puntos de agua al mapa 
    for _, row in df.iterrows():
        folium.Marker(
            location=[row["Latitud"], row["Longitud"]],
            icon=Icon(color='blue', icon="tint", prefix="fa"),
            popup=row["Nombre"]
        ).add_to(m)

    # Convertir a HTML embebible
    mapa_html = m._repr_html_()
    return render(request, "index.html", {"mapa": mapa_html})
