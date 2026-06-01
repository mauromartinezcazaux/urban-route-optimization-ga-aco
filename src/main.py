# Librerías y funciones necesarias
from geopy.geocoders import Nominatim
from algoritmo_genetico import algoritmo_genetico
from algoritmo_aco import colonia_de_hormigas
from aux_functions import to_latlon, build_distance_matrix, START_IDX, CERRAR_CICLO
from print_map import pintar, marcar_numeros, indices_a_latlon, directions_geometry
from algoritmo_hibrido import ga_aco_hibrido
import folium
import time

# Inicializar el geocodificador
geolocator = Nominatim(user_agent="route_optimizer")

# Lista para almacenar coordenadas
coordenadas = []

# Direcciones a geocodificar
direcciones = [
    "Puerta del Sol, Madrid",
    "Sagrada Familia, Barcelona",
    "Plaza del Pilar, Zaragoza",
    "Catedral de Sevilla, Sevilla",
    "Ciudad de las Artes y las Ciencias, Valencia",
    "La Alhambra, Granada, España",
    "Catedral de Santiago de Compostela, Santiago de Compostela",
    "Museo Guggenheim, Bilbao",
    "Mezquita-Catedral, Córdoba",
    "Plaza Mayor, Salamanca",
    "Casco Antiguo, Toledo",
    "Catedral de Burgos, Burgos",
    "Acueducto de Segovia, Segovia",
    "Parque Natural de las Bardenas Reales, Navarra",
    "Playa de la Concha, San Sebastián",
    "Puerto de Málaga, Málaga",
    "Cabo de Gata, Almería",
    "Ciudad Encantada, Cuenca",
    "Catedral de León, León",
    "Murallas de Ávila, Ávila"
]


# Geocodificar y almacenar coordenadas
print('Codificando direcciones...\n')
for direccion in direcciones:
    loc = geolocator.geocode(direccion, timeout=20)
    if loc:
        coordenadas.append((loc.longitude, loc.latitude))
    else:
        print(f"No se encontró: {direccion}")
print('Codificación completada.')

print("\nCoordenadas:")
print(coordenadas)

# Construir matriz de distancias
D = build_distance_matrix(to_latlon(coordenadas), cache_path='distance_matrix.npy')
COORDS_LATLON = to_latlon(coordenadas)


# ALGORITMO GENÉTICO 

# Ejecución 
t0 = time.time()
mejor_ruta_ga, mejor_coste_ga = algoritmo_genetico(D)
t1 = time.time()
print(f"\nMejor ruta GA: {mejor_ruta_ga}")
print(f"Coste GA: {mejor_coste_ga:.2f} km")
print(f"Tiempo GA: {t1 - t0:.2f} segundos")

# Mapa GA
m = folium.Map(location=COORDS_LATLON[START_IDX], zoom_start=13)
coords_ga = indices_a_latlon(mejor_ruta_ga, COORDS_LATLON)
geom_ga = directions_geometry(coords_ga)
pintar(m, geom_ga, "red")
marcar_numeros(m, coords_ga, "blue",
               margin_top=10, margin_left=-8,
               dx=0.00015, dy=-0.00010, alternate=True)
m.save("ruta_ga.html")



# ALGORITMO ACO

# Ejecución
t0 = time.time()
mejor_ruta_aco, mejor_coste_aco = colonia_de_hormigas(D)
t1 = time.time()
print(f"\nMejor ruta ACO: {mejor_ruta_aco}")
print(f"Coste ACO: {mejor_coste_aco:.2f} km")
print(f"Tiempo ACO: {t1 - t0:.2f} segundos")

# Mapa ACO
m = folium.Map(location=COORDS_LATLON[START_IDX], zoom_start=13)
coords_aco = indices_a_latlon(mejor_ruta_aco, COORDS_LATLON)
geom_aco = directions_geometry(coords_aco)  
pintar(m, geom_aco, "green")
marcar_numeros(m, coords_aco, "darkred",
               margin_top=-10, margin_left=8,
               dx=-0.00015, dy=0.00010, alternate=True)
m.save("ruta_aco.html")


# ALGORITMO HÍBRIDO GA + ACO

# Ejecución
t0 = time.time()
mejor_ruta_hibrido, mejor_coste_hibrido, elite = ga_aco_hibrido(D,
    # parámetros GA
    n_runs_ga=5,
    generaciones_ga=100,
    pop_size=50,
    pm=0.2,
    k=5,
    elitismo=5,
    # parámetros ACO
    alpha=1.0,
    beta=5.0,
    rho=0.5,
    Q=100,
    n_hormigas=50,
    n_iteraciones=100,
    start_idx=START_IDX,
    cerrar_ciclo=CERRAR_CICLO
)
t1 = time.time()
print(f"\nMejor ruta Híbrido GA+ACO: {mejor_ruta_hibrido}")
print(f"Coste Híbrido GA+ACO: {mejor_coste_hibrido:.2f} km")
print(f"Tiempo Híbrido GA+ACO: {t1 - t0:.2f} segundos")

# Mapa Híbrido GA + ACO
m = folium.Map(location=COORDS_LATLON[START_IDX], zoom_start=13)
coords_hibrido = indices_a_latlon(mejor_ruta_hibrido, COORDS_LATLON)
geom_hibrido = directions_geometry(coords_hibrido)
pintar(m, geom_hibrido, "purple")
marcar_numeros(m, coords_hibrido, "orange",
               margin_top=0, margin_left=0,
               dx=0.0, dy=0.0, alternate=True)  
m.save("ruta_hibrido.html")


