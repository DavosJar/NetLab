from enum import Enum
from typing import Dict, FrozenSet, Optional, Set, Tuple


class AFN:
    """
    Autómata Finito No Determinista (AFN).

    Representa formalmente una 5-tupla (Q, Σ, δ, q0, F) donde:
        Q  = conjunto de estados
        Σ  = alfabeto (símbolos + opcionalmente 'ε')
        δ  = función de transición  Q × Σ → P(Q)
        q0 = estado inicial
        F  = conjunto de estados de aceptación

    Las transiciones épsilon se representan con la clave 'ε' en la tabla.
    """

    EPSILON = 'ε'

    def __init__(
        self,
        nombre: str,
        alfabeto: Set[str],
        estados: Set[str],
        estado_inicial: str,
        estados_aceptacion: Set[str],
        tabla_transiciones: Dict[str, Dict[str, Tuple[str, ...]]]
    ) -> None:
        """
        Inicializa el AFN con todos sus componentes formales.

        Args:
            nombre:              Identificador descriptivo del autómata.
            alfabeto:            Conjunto de símbolos válidos (sin incluir 'ε').
            estados:             Conjunto de nombres de todos los estados.
            estado_inicial:      Estado desde el que inicia el cómputo.
            estados_aceptacion:  Estados que representan aceptación de la cadena.
            tabla_transiciones:  Función δ como diccionario anidado.
                                 Formato: {estado: {simbolo: (estados_destino,)}}
                                 Usar clave AFN.EPSILON para transiciones ε.
        """
        self.nombre = nombre
        self.alfabeto = frozenset(alfabeto)
        self.estados = frozenset(estados)
        self.estado_inicial = estado_inicial
        self.estados_aceptacion = frozenset(estados_aceptacion)
        self.tabla_transiciones = tabla_transiciones

    def transicion(self, estado: str, simbolo: str) -> Tuple[str, ...]:
        """
        Retorna los estados destino desde un estado dado con un símbolo.

        Args:
            estado:  Estado origen.
            simbolo: Símbolo leído (o AFN.EPSILON para transición vacía).

        Returns:
            Tupla de estados destino. Tupla vacía si no hay transición.
        """
        return self.tabla_transiciones.get(estado, {}).get(simbolo, ())

    def cerradura_epsilon(self, estados: Set[str]) -> FrozenSet[str]:
        """
        Calcula la cerradura-ε de un conjunto de estados.

        La cerradura-ε(S) es el conjunto de todos los estados
        alcanzables desde S siguiendo únicamente transiciones ε.

        Args:
            estados: Conjunto de estados de partida.

        Returns:
            FrozenSet con todos los estados alcanzables por ε.
        """
        pila = list(estados)
        resultado = set(estados)

        while pila:
            estado = pila.pop()
            for destino in self.transicion(estado, self.EPSILON):
                if destino not in resultado:
                    resultado.add(destino)
                    pila.append(destino)

        return frozenset(resultado)

    def mover(self, estados: Set[str], simbolo: str) -> FrozenSet[str]:
        """
        Calcula el conjunto de estados alcanzables desde un conjunto
        de estados leyendo un símbolo del alfabeto.

        Args:
            estados: Conjunto de estados de partida.
            simbolo: Símbolo a consumir.

        Returns:
            FrozenSet con todos los estados destino posibles.
        """
        resultado = set()

        for estado in estados:
            for destino in self.transicion(estado, simbolo):
                resultado.add(destino)

        return frozenset(resultado)

    def validar(self, cadena: str) -> bool:
        estados_actuales = self.cerradura_epsilon({self.estado_inicial})

        for simbolo in cadena:
            estados_actuales = self.cerradura_epsilon(
                self.mover(estados_actuales, simbolo)
            )

        return bool(estados_actuales & self.estados_aceptacion)

    def __repr__(self) -> str:
        return (
            f"AFN(nombre='{self.nombre}', "
            f"estados={len(self.estados)}, "
            f"aceptacion={set(self.estados_aceptacion)})"
        )
