from django.shortcuts import render
import pandas as pd
import pyproj
import folium
from folium import Icon
from django.conf import settings
import os

def index(request):
    csv_path = os.path.join(settings.BASE_DIR, "data", "datos.csv")

    df = pd.read_csv(
        csv_path,
        sep=",",
        engine="python",
        quoting=3,       
        on_bad_lines="skip",
        encoding="latin-1",
    )
    
    for col in ("UTM_ESTE", "UTM_NORTE", "CAUDAL"):
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Limpiar strings
    df["COMUNA"]            = df["COMUNA"].astype(str).str.strip()
    df["NOM_SUBSUBCUENCA"]  = df["NOM_SUBSUBCUENCA"].fillna("No hay registro").astype(str).str.strip()
    df["NOM_CUENCA"]        = df["NOM_CUENCA"].astype(str).str.strip()

    # Quitar filas que no ocuparemos
    df = df.dropna(subset=["UTM_ESTE", "UTM_NORTE", "CAUDAL", "COMUNA", "NOM_SUBSUBCUENCA", "NOM_CUENCA"])

    # Comunas y sub-subcuencas únicas para los select
    comunas        = [""] + sorted(df["COMUNA"].unique())
    subsubcuencas  = [""] + sorted(df["NOM_SUBSUBCUENCA"].unique())

    # Agrupar por coordenada y calcular promedio de caudal
    grp = (
        df.groupby(["UTM_ESTE","UTM_NORTE"], as_index=False)
          .agg({
             "CAUDAL": "mean",
             "COMUNA": lambda s: s.mode().iat[0],
             "NOM_CUENCA": lambda s: s.mode().iat[0],
             "NOM_SUBSUBCUENCA": lambda s: s.mode().iat[0],
          })
          .rename(columns={"CAUDAL":"AVG_CAUDAL"})
    )

    # Rango de caudal promedio
    min_avg = grp["AVG_CAUDAL"].min()
    max_avg = grp["AVG_CAUDAL"].max()

    # Leer valores de filtro del GET
    comuna_sel    = request.GET.get("comuna", "")
    subsel        = request.GET.get("subsub", "")
    sel_min       = request.GET.get("min_avg", f"{min_avg:.2f}")
    sel_max       = request.GET.get("max_avg", f"{max_avg:.2f}")

    try:
        sel_min = float(sel_min)
        sel_max = float(sel_max)
    except ValueError:
        sel_min, sel_max = min_avg, max_avg

    # Aplicar filtros
    if comuna_sel:
        grp = grp[grp["COMUNA"] == comuna_sel]
    if subsel:
        grp = grp[grp["NOM_SUBSUBCUENCA"] == subsel]

    grp = grp[(grp["AVG_CAUDAL"] >= sel_min) & (grp["AVG_CAUDAL"] <= sel_max)]

    # Proyección UTM → WGS84
    transformer = pyproj.Transformer.from_crs("epsg:32719","epsg:4326",always_xy=True)

    # Crear mapa y marcadores
    m = folium.Map(location=[-33.45, -70.67], zoom_start=6, tiles="CartoDB.Positron")
    for _, row in grp.iterrows():
        lon, lat = transformer.transform(row["UTM_ESTE"], row["UTM_NORTE"])
        popup = (
            f"<strong>Cuenca:</strong> {row['NOM_CUENCA']}<br>"
            f"<strong>Sub-subcuenca:</strong> {row['NOM_SUBSUBCUENCA']}<br>"
            f"<strong>Comuna:</strong> {row['COMUNA']}<br>"
            f"<strong>Caudal promedio:</strong> {row['AVG_CAUDAL']:.2f} m³/s"
        )
        folium.Marker(
            location=[lat,lon],
            popup=popup,
            icon=Icon(color="blue", icon="tint", prefix="fa")
        ).add_to(m)
    
    # Renderizar
    return render(request, "index.html", {
        "mapa":         m._repr_html_(),
        "comunas":      comunas,
        "subsubs":      subsubcuencas,
        "min_avg":      f"{min_avg:.2f}",
        "max_avg":      f"{max_avg:.2f}",
        "sel_min":      f"{sel_min:.2f}",
        "sel_max":      f"{sel_max:.2f}",
        "comuna_sel":   comuna_sel,
        "subsel":       subsel,
    })
