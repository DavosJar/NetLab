from Dominio_automatas.modelos.afn import AFN
from Dominio_automatas.operaciones.repetir import repetir
from Dominio_automatas.automatas.segmento_hex import construir_afn_segmento_hex
from Dominio_automatas.automatas.separador_mac import construir_afn_separador_mac

def construir_afn_mac() -> AFN:
    """
    Construye el AFN que reconoce una dirección MAC válida.
    
    Lenguaje: segmento_hex : segmento_hex : segmento_hex : segmento_hex : segmento_hex : segmento_hex
    (6 segmentos hexadecimales separados por 5 delimitadores de dos puntos ':')
    """
    afn_segmento = construir_afn_segmento_hex()
    afn_separador = construir_afn_separador_mac()

    return repetir(afn_segmento, n=6, separador=afn_separador)
