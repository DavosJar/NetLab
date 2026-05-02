from Dominio_automatas.modelos.afn import AFN
import itertools

_contador = itertools.count()


def _renombrar_estados(afn: 'AFN', prefijo: str) -> tuple[dict, dict]:
    """
    Renombra todos los estados de un AFN agregando un prefijo.

    Args:
        afn:     AFN cuyos estados se renombrarán.
        prefijo: Prefijo a agregar a cada estado.

    Returns:
        Tupla (mapa, tabla) donde:
            mapa:  {estado_original: estado_renombrado}
            tabla: tabla de transiciones con estados renombrados
    """
    # 1. Construir mapa de renombrado
    mapa = {estado: f"{prefijo}_{estado}" for estado in afn.estados}


    tabla = {}
    for estado, transiciones in afn.tabla_transiciones.items():
        nuevo_estado = mapa[estado]
        tabla[nuevo_estado] = {}
        for simbolo, destinos in transiciones.items():
            tabla[nuevo_estado][simbolo] = tuple(mapa[d] for d in destinos)

    return mapa, tabla

def concatenar(afn_a: AFN, afn_b: AFN) -> AFN:
    """
    Construye un nuevo AFN que reconoce la concatenación
    L(afn_a) · L(afn_b).

    Conecta los estados de aceptación de afn_a al estado
    inicial de afn_b mediante transiciones ε.

    Args:
        afn_a: AFN izquierdo.
        afn_b: AFN derecho.

    Returns:
        Nuevo AFN que reconoce L(afn_a) · L(afn_b).
    """
    # 1. Renombrar estados para evitar colisiones
    id_a = next(_contador)
    id_b = next(_contador)
    mapa_a, tabla_a = _renombrar_estados(afn_a, str(id_a))
    mapa_b, tabla_b = _renombrar_estados(afn_b, str(id_b))

    # 2. Estado inicial y aceptación renombrados
    inicial_a      = mapa_a[afn_a.estado_inicial]
    aceptacion_a   = {mapa_a[e] for e in afn_a.estados_aceptacion}
    inicial_b      = mapa_b[afn_b.estado_inicial]
    aceptacion_b   = {mapa_b[e] for e in afn_b.estados_aceptacion}

    # 3. Agregar ε desde cada estado final de afn_a al inicial de afn_b
    for estado_final in aceptacion_a:
        tabla_a[estado_final][AFN.EPSILON] = (inicial_b,)

    # 4. Unir tablas, estados y alfabetos
    tabla_unida  = {**tabla_a, **tabla_b}
    estados      = set(mapa_a.values()) | set(mapa_b.values())
    alfabeto     = afn_a.alfabeto | afn_b.alfabeto

    return AFN(
        nombre=f"{afn_a.nombre}_{afn_b.nombre}",
        alfabeto=alfabeto,
        estados=estados,
        estado_inicial=inicial_a,
        estados_aceptacion=aceptacion_b,  # solo afn_b acepta
        tabla_transiciones=tabla_unida,
    )