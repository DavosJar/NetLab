
from collections import deque
from Dominio_automatas.modelos import AFN
from Dominio_automatas.modelos import AFD


def _nombre_superestado(superestado: frozenset) -> str:
    """
    Convierte un superestado (frozenset de estados) a string legible.
    Ejemplo: frozenset({'q0', 'q1'}) → '{q0,q1}'
    """
    return '{' + ','.join(sorted(superestado)) + '}'


def afn_a_afd(afn: AFN) -> AFD:
    """
    Convierte un AFN a un AFD equivalente mediante el
    algoritmo de construcción de subconjuntos.

    Args:
        afn: AFN a convertir.

    Returns:
        AFD equivalente que reconoce el mismo lenguaje.
    """
    inicial   = afn.cerradura_epsilon({afn.estado_inicial})
    tabla_afd = {}
    estados_afd = set()
    cola      = deque([inicial])
    visitados = {inicial}

    while cola:
        actual        = cola.popleft()
        nombre_actual = _nombre_superestado(actual)
        estados_afd.add(nombre_actual)
        tabla_afd[nombre_actual] = {}

        for simbolo in sorted(afn.alfabeto):
            destino = afn.cerradura_epsilon(afn.mover(actual, simbolo))

            if not destino:
                continue

            nombre_destino = _nombre_superestado(destino)
            tabla_afd[nombre_actual][simbolo] = nombre_destino

            if destino not in visitados:
                visitados.add(destino)
                cola.append(destino)

    aceptacion_afd = {
        _nombre_superestado(s) for s in visitados
        if s & afn.estados_aceptacion
    }

    return AFD(
        nombre=f"{afn.nombre}_afd",
        alfabeto=set(afn.alfabeto),
        estados=estados_afd,
        estado_inicial=_nombre_superestado(inicial),
        estados_aceptacion=aceptacion_afd,
        tabla_transiciones=tabla_afd,
    )