from Dominio_automatas.modelos.afn import AFN

def construir_afn_octeto() -> AFN:
    """
    Construye el AFN que reconoce un octeto IPv4 válido (0-255).

    Estados:
        q0 → inicial
        q1 → acepta 1 dígito (0-9)
        q2 → intermedio 2-3 dígitos (1-9 + cualquier dígito)
        q3 → acepta 2 dígitos (10-99)
        q4 → intermedio 100-199
        q5 → intermedio 200-249
        q6 → intermedio 250-255
        q7 → intermedio 100-249 segundo dígito
        q8 → acepta 3 dígitos (100-255)
    """
    alfabeto = set('0123456789')

    tabla = {
        'q0': {
            '0': ('q1',),
            '1': ('q1', 'q2', 'q4'),
            '2': ('q1', 'q2', 'q5'),
            **{d: ('q1', 'q2') for d in '3456789'}
        },
        'q1': {**{d: () for d in '0123456789'}},
        'q2': {**{d: ('q3',) for d in '0123456789'}},
        'q3': {**{d: () for d in '0123456789'}},
        'q4': {**{d: ('q7',) for d in '0123456789'}},
        'q5': {
            **{d: ('q7',) for d in '01234'},
            '5': ('q6',),
        },
        'q6': {**{d: ('q8',) for d in '012345'}},
        'q7': {**{d: ('q8',) for d in '0123456789'}},
        'q8': {**{d: () for d in '0123456789'}},
    }

    return AFN(
        nombre='octeto_ipv4',
        alfabeto=alfabeto,
        estados={'q0','q1','q2','q3','q4','q5','q6','q7','q8'},
        estado_inicial='q0',
        estados_aceptacion={'q1', 'q3', 'q8'},
        tabla_transiciones=tabla,
    )