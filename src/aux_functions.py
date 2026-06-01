import os
import numpy as np
import openrouteservice

START_IDX = 0
CERRAR_CICLO = False

# Configuración de la API de OpenRouteService
client = openrouteservice.Client(key='eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6ImFmYjllN2I5OWI2MzRmY2M4ZWMyYzU4YWE0NDAxOWM2IiwiaCI6Im11cm11cjY0In0=')

# Helpers orden coordenadas
def to_lonlat(coords):
    return [[lon, lat] for (lat, lon) in coords]

def to_latlon(coords):
    return [[lat, lon] for (lon, lat) in coords]

# Construcción de la matriz de distancias 
def build_distance_matrix(coords_latlon, cache_path='distance_matrix.npy'):
    if os.path.exists(cache_path):
        return np.load(cache_path)
    lonlat = to_lonlat(coords_latlon)
    resp = client.distance_matrix(
        locations=lonlat,
        profile='driving-car',
        metrics=['distance'],
        resolve_locations=False,
        validate=True
    )
    D = np.array(resp['distances'], dtype=float) / 1000.0  # Convertir a km
    np.save(cache_path, D)
    return D

# Cálculo del coste de una ruta
def coste_ruta_idx(ruta, D, cerrar_ciclo=False):
    dist = sum(D[ruta[i], ruta[i+1]] for i in range(len(ruta)-1))
    if cerrar_ciclo:
        dist += D[ruta[-1], ruta[0]]
    return dist