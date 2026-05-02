from collections import deque
from Dominio_automatas.modelos.afd import AFD

def _estados_alcanzables(afd: AFD) -> frozenset:
    """Calcula estados alcanzables desde el estado inicial."""
    visitados = set()
    pila = [afd.estado_inicial]

    while pila:
        actual = pila.pop()
        if actual in visitados:
            continue
        visitados.add(actual)
        for simbolo in afd.alfabeto:
            destino = afd.transicion(actual, simbolo)
            if destino != AFD.ESTADO_TRAMPA and destino not in visitados:
                pila.append(destino)

    return frozenset(visitados)


def _tabla_distincion(afd: AFD, estados: list) -> dict:
    tabla = {}

    for i in range(len(estados)):
        for j in range(i + 1, len(estados)):
            a, b = estados[i], estados[j]
            es_aceptacion_a = a in afd.estados_aceptacion
            es_aceptacion_b = b in afd.estados_aceptacion
            tabla[(a, b)] = es_aceptacion_a != es_aceptacion_b

    cambio = True
    while cambio:
        cambio = False
        for par, distinguible in list(tabla.items()):
            if distinguible:
                continue
            a, b = par
            for simbolo in afd.alfabeto:
                destino_a = afd.transicion(a, simbolo)
                destino_b = afd.transicion(b, simbolo)

                # si van al mismo lado no distingue
                if destino_a == destino_b:
                    continue

                # si uno va a trampa y el otro no → distinguibles
                if destino_a == AFD.ESTADO_TRAMPA or destino_b == AFD.ESTADO_TRAMPA:
                    tabla[par] = True
                    cambio = True
                    break

                par_destinos = (
                    (destino_a, destino_b)
                    if (destino_a, destino_b) in tabla
                    else (destino_b, destino_a)
                )
                if tabla.get(par_destinos, False):
                    tabla[par] = True
                    cambio = True
                    break

    return tabla


def _agrupar(estados: list, tabla: dict) -> list:
    """
    Agrupa estados indistinguibles usando union-find simple.
    Retorna lista de grupos (sets de estados equivalentes).
    """
    representante = {e: e for e in estados}

    def encontrar(e):
        while representante[e] != e:
            e = representante[e]
        return e

    for (a, b), distinguible in tabla.items():
        if not distinguible:
            ra, rb = encontrar(a), encontrar(b)
            if ra != rb:
                representante[rb] = ra

    grupos = {}
    for e in estados:
        r = encontrar(e)
        if r not in grupos:
            grupos[r] = set()
        grupos[r].add(e)

    return list(grupos.values())


def minimizar(afd: AFD) -> AFD:
    """
    Construye el AFD mínimo equivalente mediante Table-Filling.

    Args:
        afd: AFD a minimizar.

    Returns:
        Nuevo AFD mínimo que reconoce el mismo lenguaje.
    """
    # 1. Eliminar inalcanzables
    alcanzables = _estados_alcanzables(afd)
    estados     = sorted(alcanzables)

    # 2. Tabla de distincion
    tabla = _tabla_distincion(afd, estados)

    # 3. Agrupar indistinguibles
    grupos = _agrupar(estados, tabla)

    # 4. Representante de cada grupo = primer estado ordenado
    rep = {}
    for grupo in grupos:
        representante = sorted(grupo)[0]
        for e in grupo:
            rep[e] = representante

    # 5. Construir tabla minimizada
    tabla_min = {}
    for grupo in grupos:
        r = sorted(grupo)[0]
        tabla_min[r] = {}
        for simbolo in afd.alfabeto:
            destino = afd.transicion(r, simbolo)
            if destino != AFD.ESTADO_TRAMPA:
                tabla_min[r][simbolo] = rep[destino]

    estados_min     = {sorted(g)[0] for g in grupos}
    aceptacion_min  = {rep[e] for e in afd.estados_aceptacion if e in alcanzables}
    inicial_min     = rep[afd.estado_inicial]

    return AFD(
        nombre=f"{afd.nombre}_min",
        alfabeto=set(afd.alfabeto),
        estados=estados_min,
        estado_inicial=inicial_min,
        estados_aceptacion=aceptacion_min,
        tabla_transiciones=tabla_min,
    )