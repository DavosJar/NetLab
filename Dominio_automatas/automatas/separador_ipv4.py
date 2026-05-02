from Dominio_automatas.modelos.afn import AFN

def construir_afn_punto() -> AFN:
    """
    Construye el AFN que reconoce el separador de IPv4.

    Lenguaje: { '.' }

    Estados:
        q0 → inicial
        q1 → acepta, se leyó '.'
    """
    return AFN(
        nombre='separador_ipv4',
        alfabeto={'.'},
        estados={'q0', 'q1'},
        estado_inicial='q0',
        estados_aceptacion={'q1'},
        tabla_transiciones={
            'q0': {'.': ('q1',)},
            'q1': {},
        }
    )