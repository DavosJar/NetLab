from Dominio_automatas.modelos.afn import AFN
from Dominio_automatas.operaciones.concatenar import concatenar


def _clonar(afn: AFN, indice: int) -> AFN:
    """
    Crea una copia del AFN con estados renombrados usando un índice
    para evitar colisiones al concatenar múltiples copias.

    Args:
        afn:    AFN a clonar.
        indice: Índice único para diferenciar esta copia.

    Returns:
        Nuevo AFN con estados renombrados.
    """
    prefijo = f"{indice}"  # solo el índice, sin el nombre acumulado
    mapa = {estado: f"{prefijo}_{estado}" for estado in afn.estados}

    tabla = {}
    for estado, transiciones in afn.tabla_transiciones.items():
        nuevo_estado = mapa[estado]
        tabla[nuevo_estado] = {}
        for simbolo, destinos in transiciones.items():
            tabla[nuevo_estado][simbolo] = tuple(mapa[d] for d in destinos)

    return AFN(
        nombre=f"{afn.nombre}_{indice}",
        alfabeto=set(afn.alfabeto),
        estados=set(mapa.values()),
        estado_inicial=mapa[afn.estado_inicial],
        estados_aceptacion={mapa[e] for e in afn.estados_aceptacion},
        tabla_transiciones=tabla,
    )


def repetir(afn: AFN, n: int, separador: AFN = None) -> AFN:
    """
    Repite un AFN exactamente n veces, opcionalmente con separador.

    Estructura:
        afn · (separador · afn) · (separador · afn) · ... (n-1 veces)

    Args:
        afn:       AFN a repetir.
        n:         Número de repeticiones (n >= 1).
        separador: AFN opcional intercalado entre repeticiones.

    Returns:
        AFN que reconoce L(afn) [separador L(afn)] * (n-1).

    Raises:
        ValueError: Si n < 1.
    """
    if n < 1:
        raise ValueError(f"n debe ser >= 1, se recibió {n}")

    # construir lista de bloques: [afn_0, sep_1+afn_1, sep_2+afn_2, ...]
    bloques = [_clonar(afn, 0)]
    for i in range(1, n):
        if separador is not None:
            bloque = concatenar(_clonar(separador, i), _clonar(afn, i))
        else:
            bloque = _clonar(afn, i)
        bloques.append(bloque)

    # concatenar todos los bloques en orden
    resultado = bloques[0]
    for bloque in bloques[1:]:
        resultado = concatenar(resultado, bloque)

    return resultado
