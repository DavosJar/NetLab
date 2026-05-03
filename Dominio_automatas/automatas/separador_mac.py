from Dominio_automatas.modelos.afn import AFN

def construir_afn_separador_mac() -> AFN:
    """
    Construye el AFN que reconoce el separador de direcciones MAC.

    Lenguaje: { ':' }

    Estados:
        q0 → inicial
        q1 → acepta, se leyó ':'
    """
    return AFN(
        nombre='separador_mac',
        alfabeto={':'},
        estados={'q0', 'q1'},
        estado_inicial='q0',
        estados_aceptacion={'q1'},
        tabla_transiciones={
            'q0': {':': ('q1',)},
            'q1': {},
        }
    )