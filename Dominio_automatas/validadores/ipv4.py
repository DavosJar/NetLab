from Dominio_automatas.modelos.afn import AFN
from Dominio_automatas.operaciones.concatenar import concatenar
from Dominio_automatas.operaciones.repetir import repetir
from Dominio_automatas.automatas.octeto import construir_afn_octeto
from Dominio_automatas.automatas.separador_ipv4 import construir_afn_punto

def construir_afn_ipv4() -> AFN:
    """
    Construye el AFN que reconoce una dirección IPv4 válida.
    Lenguaje: octeto . octeto . octeto . octeto
    """
    afn_octeto = construir_afn_octeto()
    afn_punto  = construir_afn_punto()

    return repetir(afn_octeto, n=4, separador=afn_punto)