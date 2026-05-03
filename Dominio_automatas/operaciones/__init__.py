"""
Módulo de operaciones: funciones para construir, combinar y transformar autómatas.
"""

from .concatenar import concatenar
from .repetir import repetir
from .subconjuntos import afn_a_afd
from .minimizar import minimizar

__all__ = ["concatenar", "union", "repetir", "afn_a_afd", "minimizar"]
