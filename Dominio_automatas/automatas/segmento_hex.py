from Dominio_automatas.modelos.afn import AFN

def construir_afn_segmento_hex() -> AFN:
    """
    Construye el AFN que reconoce un par hexadecimal válido para direcciones MAC.

    Lenguaje: { 2 caracteres de '0123456789abcdefABCDEF' }

    Estados:
        q0 → inicial
        q1 → intermedio, se leyó el primer carácter
        q2 → acepta, se leyó el segundo carácter (par completo)
    """
    alfabeto_hex = {
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
        'a', 'b', 'c', 'd', 'e', 'f',
        'A', 'B', 'C', 'D', 'E', 'F'
    }

    # Definimos la transición a usar en cada estado
    transicion_a_q1 = {char: ('q1',) for char in alfabeto_hex}
    transicion_a_q2 = {char: ('q2',) for char in alfabeto_hex}

    return AFN(
        nombre='segmento_hex_mac',
        alfabeto=alfabeto_hex,
        estados={'q0', 'q1', 'q2'},
        estado_inicial='q0',
        estados_aceptacion={'q2'},
        tabla_transiciones={
            'q0': transicion_a_q1,
            'q1': transicion_a_q2,
            'q2': {},
        }
    )