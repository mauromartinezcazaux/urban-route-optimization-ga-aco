from algoritmo_genetico import algoritmo_genetico
from algoritmo_aco import colonia_de_hormigas
import numpy as np

def ga_elite_set(D, n_runs, generaciones, pop_size, pm, k, elitismo, start_idx=0):
    elite = []
    for _ in range(n_runs):
        ruta, coste = algoritmo_genetico(D, generaciones, pop_size, pm, k, elitismo, start_idx)
        elite.append((ruta, coste))
    elite.sort(key=lambda x: x[1])
    return elite

def construir_tau_inicial(elite, D, refuerzo=1.0):
    n = len(D)
    tau = np.zeros((n, n))

    for ruta, coste in elite:
        aporte = refuerzo / coste
        for i in range(len(ruta) - 1):
            a, b = ruta[i], ruta[i+1]
            tau[a, b] += aporte

    tau += 1e-6
    return tau

def ga_aco_hibrido(D,
                   # parámetros GA
                   n_runs_ga, generaciones_ga, pop_size, pm, k, elitismo,
                   # parámetros ACO
                   alpha, beta, rho, Q, n_hormigas, n_iteraciones,
                   start_idx=0, cerrar_ciclo=False):
    
    # Fase GA: obtener conjunto elite
    elite = ga_elite_set(D, n_runs_ga, generaciones_ga, pop_size, pm, k, elitismo, start_idx)

    # Construir tau inicial a partir del conjunto elite
    tau_init = construir_tau_inicial(elite, D, refuerzo=1.0)

    # Fase ACO: ejecutar con tau inicial
    mejor_ruta, mejor_coste = colonia_de_hormigas(
        D, alpha, beta, rho, Q, n_hormigas, n_iteraciones,
        start_idx=start_idx, cerrar_ciclo=cerrar_ciclo, tau_init=tau_init
    )

    return mejor_ruta, mejor_coste, elite

