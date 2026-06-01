from aux_functions import client
import folium
import math

def directions_geometry(coords_latlon_ordenadas):
    """
    Une cada par consecutivo con ORS (driving-car), evitando el límite 6.000 km.
    - Valida/corrige (lat,lon) por si hay swaps.
    - Reintenta con radiuses mayores.
    - Si un tramo falla: línea recta para ese tramo.
    Devuelve lista de (lat,lon) lista para folium.
    """

    full_geom_lonlat = []  # acumulamos en (lon,lat) para luego invertir 1 sola vez
    for i in range(len(coords_latlon_ordenadas) - 1):
        lat1, lon1 = coords_latlon_ordenadas[i]
        lat2, lon2 = coords_latlon_ordenadas[i+1]
        seg_lonlat = [[lon1, lat1], [lon2, lat2]]  # ORS (lon,lat)

        # Reintentos escalando radiuses
        ok = False
        for rad in (1500, 3000, 5000):
            try:
                r = client.directions(
                    coordinates=seg_lonlat,
                    profile='driving-car',
                    format='geojson',
                    radiuses=[rad, rad]
                )
                geom = r['features'][0]['geometry']['coordinates'] 
                if full_geom_lonlat and geom:
                    full_geom_lonlat.extend(geom[1:])  # evita duplicar nodo
                else:
                    full_geom_lonlat.extend(geom)
                ok = True
                break
            except Exception as e:
                # Si falla, probamos con radio mayor
                continue

        if not ok:
            # Último recurso: línea recta entre los puntos (no paramos el mapa)
            if full_geom_lonlat:
                full_geom_lonlat.append([lon2, lat2])
            else:
                full_geom_lonlat.extend([[lon1, lat1], [lon2, lat2]])

    # Convertimos todo a (lat,lon) para folium una sola vez
    return [(lat, lon) for (lon, lat) in full_geom_lonlat]

def indices_a_latlon(ruta_idx, coords_latlon):
    return [coords_latlon[i] for i in ruta_idx]

def pintar(m, latlon_geom, color):
    c = str(color).lower()
    if c == "green":  # ACO debajo (halo ancho semitransparente)
        folium.PolyLine(latlon_geom, color='green', weight=10, opacity=0.8).add_to(m)
    elif c == "red":  # GA encima (fino y discontinuo)
        folium.PolyLine(latlon_geom, color='red',   weight=4,  opacity=0.95, dash_array='8,6').add_to(m)
    else:             # fallback
        folium.PolyLine(latlon_geom, color=color,   weight=5,  opacity=0.8).add_to(m)



def marcar_numeros(m, coords_latlon_ordenadas, color,
                   margin_top=-10, margin_left=8,
                   dx=0.0, dy=0.0, alternate=False, outline=True):
    """
    dx, dy: desplazamiento en grados (~0.0001 ≈ 11 m en lat).
    alternate=True alterna el signo por punto (evita solapes).
    outline=True dibuja contorno blanco para legibilidad.
    """
    shadow = ("text-shadow: -1px -1px 0 #fff, 1px -1px 0 #fff, "
              " -1px 1px 0 #fff, 1px 1px 0 #fff;") if outline else ""
    for i, (lat, lon) in enumerate(coords_latlon_ordenadas, start=1):
        s = (1 if (not alternate or i % 2) else -1)
        lon_adj = lon + (dx * s) / max(1e-9, math.cos(math.radians(lat)))
        lat_adj = lat + (dy * s)
        folium.Marker(
            [lat_adj, lon_adj],
            icon=folium.DivIcon(html=(
                f'<div style="font-size:16px; color:{color}; {shadow}'
                f'margin-top:{margin_top}px; margin-left:{margin_left}px;"><b>{i}</b></div>'
            )),
            z_index_offset=1000
        ).add_to(m)

