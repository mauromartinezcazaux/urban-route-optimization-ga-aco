from aux_functions import coste_ruta_idx, START_IDX, CERRAR_CICLO
import numpy as np
import random

def colonia_de_hormigas(
    D, alpha=1.0, beta=5.0, rho=0.5, Q=100,
    n_hormigas=50, n_iteraciones=200, start_idx=START_IDX, cerrar_ciclo=CERRAR_CICLO, tau_init=None
):
    n = D.shape[0]
    if tau_init is None: 
        tau = np.ones((n, n)) 
    else: 
        tau = tau_init.copy()    # feromonas
    eta = 1.0 / (D + 1e-12)                    # visibilidad (1/dist)
    mejor_ruta_aco, mejor_coste_aco = None, float('inf')

    for _ in range(n_iteraciones):
        rutas = []
        for _a in range(n_hormigas):
            ruta = [start_idx]
            no_visitados = set(range(n)) - {start_idx}
            while no_visitados:
                i = ruta[-1]
                candidatos = list(no_visitados)
                # Probabilidades (tau^alpha * eta^beta) con salvaguarda
                pesos = [(tau[i, j]**alpha) * (eta[i, j]**beta) for j in candidatos]
                if not any(w > 0 for w in pesos):
                    # Si todo es 0 (numerical underflow o distancias imposibles), elegir uniforme
                    j_next = random.choice(candidatos)
                else:
                    j_next = random.choices(candidatos, weights=pesos, k=1)[0]
                ruta.append(j_next)
                no_visitados.remove(j_next)
            rutas.append(ruta)

        # Actualiza mejor
        for r in rutas:
            c = coste_ruta_idx(r, D, cerrar_ciclo)
            if c < mejor_coste_aco:
                mejor_ruta_aco, mejor_coste_aco = r, c

        # Evaporación
        tau *= (1.0 - rho)

        # Depósito
        for r in rutas:
            c = coste_ruta_idx(r, D, cerrar_ciclo)
            if c <= 0:      
                continue
            delta = Q / c
            for a, b in zip(r[:-1], r[1:]):
                tau[a, b] += delta
            if cerrar_ciclo:
                tau[r[-1], r[0]] += delta

    
    return mejor_ruta_aco, mejor_coste_aco
