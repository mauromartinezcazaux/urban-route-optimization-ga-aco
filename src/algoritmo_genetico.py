from aux_functions import coste_ruta_idx, START_IDX, CERRAR_CICLO
import random

def torneo(poblacion, k, D):
    k = min(k, len(poblacion))
    candidatos = random.sample(poblacion, k)
    return min(candidatos, key=lambda ruta: coste_ruta_idx(ruta, D, CERRAR_CICLO))

def cruce(padre1, padre2):
    # OX manteniendo start fijo en posición 0
    n = len(padre1)
    a, b = sorted(random.sample(range(1, n), 2))  # no tocamos el índice 0
    hijo = [None] * n
    hijo[0] = padre1[0]
    hijo[a:b] = padre1[a:b]
    # Relleno en orden relativo desde padre2, sin duplicados
    fill = [x for x in padre2 if x not in hijo]
    j = 0
    for i in range(1, n):
        if hijo[i] is None:
            hijo[i] = fill[j]
            j += 1
    return hijo

def mutacion(ruta):
    # swap mutation sin mover el índice 0
    i, j = sorted(random.sample(range(1, len(ruta)), 2))
    r = ruta[:]               # copiar
    r[i], r[j] = r[j], r[i]   # intercambiar
    return r

def algoritmo_genetico(D, generaciones=200, pop_size=80, pm=0.2, k=3, elitismo=2, start_idx=START_IDX, cerrar_ciclo=CERRAR_CICLO):
    assert pop_size >= 4, "pop_size debe ser >= 4"
    n = D.shape[0]
    base = [i for i in range(n) if i != start_idx]

    # Población inicial (todas empiezan en start_idx)
    poblacion = [[start_idx] + random.sample(base, len(base)) for _ in range(pop_size)]

    mejor_ruta = min(poblacion, key=lambda r: coste_ruta_idx(r, D, cerrar_ciclo))
    mejor_coste = coste_ruta_idx(mejor_ruta, D, cerrar_ciclo)

    for _ in range(generaciones):
        # Elitismo
        elite = sorted(poblacion, key=lambda r: coste_ruta_idx(r, D, cerrar_ciclo))[:elitismo]
        nueva_poblacion = elite[:]

        # Reproducción (generar todos los hijos)
        parejas = max(1, (pop_size - len(nueva_poblacion)) // 2)
        for __ in range(parejas):
            p1 = torneo(poblacion, k, D)
            p2 = torneo(poblacion, k, D)
            h1 = cruce(p1, p2)
            h2 = cruce(p2, p1)
            if random.random() < pm: h1 = mutacion(h1)
            if random.random() < pm: h2 = mutacion(h2)
            nueva_poblacion.extend([h1, h2])

        # Completar si faltan individuos 
        while len(nueva_poblacion) < pop_size:
            nueva_poblacion.append([start_idx] + random.sample(base, len(base)))

        # Selección generacional
        poblacion = sorted(nueva_poblacion, key=lambda r: coste_ruta_idx(r, D, cerrar_ciclo))[:pop_size]

        # Actualizar mejor global
        cand = poblacion[0]
        cand_cost = coste_ruta_idx(cand, D, cerrar_ciclo)
        if cand_cost < mejor_coste:
            mejor_ruta, mejor_coste = cand, cand_cost

    return mejor_ruta, mejor_coste
