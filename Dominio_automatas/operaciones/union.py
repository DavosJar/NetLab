"""
Operación de unión: construir AFN que reconoce L(A) ∪ L(B).

Algoritmo:
    1. Crear nuevo estado inicial.
    2. Conectar nuevos estados iniciales con ε-transiciones a estados iniciales de ambos AFN.
"""


def union(afn_a, afn_b):
    """
    Une dos AFN: reconoce L(afn_a) ∪ L(afn_b).
    
    Args:
        afn_a: Primer AFN (A).
        afn_b: Segundo AFN (B).
        
    Returns:
        AFN que reconoce L(A) ∪ L(B).
    """
    ...
