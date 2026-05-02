from typing import Dict, FrozenSet, Optional, Set, Tuple


class AFD:
    """
    Autómata Finito Determinista (AFD).

    Representa formalmente una 5-tupla (Q, Σ, δ, q0, F) donde:
        Q  = conjunto de estados
        Σ  = alfabeto de símbolos
        δ  = función de transición TOTAL  Q × Σ → Q
        q0 = estado inicial
        F  = conjunto de estados de aceptación

    A diferencia del AFN, δ retorna exactamente un estado por par
    (estado, símbolo). Los pares sin transición apuntan al estado
    trampa (dead state).
    """

    ESTADO_TRAMPA = "∅"

    def __init__(
        self,
        nombre: str,
        alfabeto: Set[str],
        estados: Set[str],
        estado_inicial: str,
        estados_aceptacion: Set[str],
        tabla_transiciones: Dict[str, Dict[str, str]],
    ) -> None:
        """
        Inicializa el AFD con todos sus componentes formales.

        Args:
            nombre:             Identificador descriptivo del autómata.
            alfabeto:           Conjunto de símbolos válidos.
            estados:            Conjunto de nombres de todos los estados.
            estado_inicial:     Estado desde el que inicia el cómputo.
            estados_aceptacion: Estados que representan aceptación.
            tabla_transiciones: Función δ como diccionario anidado.
                                Formato: {estado: {simbolo: estado_destino}}
                                Pares ausentes se tratan como estado trampa.
        """
        self.nombre = nombre
        self.alfabeto = frozenset(alfabeto)
        self.estados = frozenset(estados)
        self.estado_inicial = estado_inicial
        self.estados_aceptacion = frozenset(estados_aceptacion)
        self.tabla_transiciones = tabla_transiciones

    def transicion(self, estado: str, simbolo: str) -> str:
        """
        Retorna el único estado destino desde un estado dado con un símbolo.

        Si no existe transición definida, retorna el estado trampa.

        Args:
            estado:  Estado origen.
            simbolo: Símbolo leído.

        Returns:
            Estado destino o AFD.ESTADO_TRAMPA si no hay transición.
        """
        return self.tabla_transiciones.get(estado, {}).get(simbolo, self.ESTADO_TRAMPA)

    def validar(self, cadena: str) -> bool:
        estado_actual = self.estado_inicial

        for simbolo in cadena:
            if simbolo not in self.alfabeto:
                estado_actual = self.ESTADO_TRAMPA
            else:
                estado_actual = self.transicion(estado_actual, simbolo)

        return estado_actual in self.estados_aceptacion


    def __repr__(self) -> str:
        return (
            f"AFD(nombre='{self.nombre}', "
            f"estados={len(self.estados)}, "
            f"aceptacion={set(self.estados_aceptacion)})"
        )