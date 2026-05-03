from Dominio_automatas.modelos.afn import AFN
from Dominio_automatas.modelos.afd import AFD
from Dominio_automatas.operaciones.subconjuntos import afn_a_afd
from Dominio_automatas.operaciones.minimizar import minimizar



class ServicioAutomata:

    def __init__(self, afn: AFN) -> None:
        self.afn     = afn
        self.afd     = afn_a_afd(afn)
        self.afd_min = minimizar(self.afd)
        self._mapa   = self._construir_mapa()

    def _construir_mapa(self) -> dict:
        """
        Construye un mapa de nombres internos a nombres legibles.
        Unifica estados de AFN, AFD y AFD mínimo en un solo mapa.
        """
        todos = (
            set(self.afn.estados) |
            set(self.afd.estados) |
            set(self.afd_min.estados)
        )
        return {
            estado: f"S{i}"
            for i, estado in enumerate(sorted(todos))
        }

    def _n(self, estado: str) -> str:
        """Traduce un estado interno a nombre legible."""
        return self._mapa.get(estado, estado)

    def _info_afn(self) -> dict:
        return {
            "nombre":     self.afn.nombre,
            "estados":    sorted(self._n(e) for e in self.afn.estados),
            "alfabeto":   sorted(self.afn.alfabeto),
            "inicial":    self._n(self.afn.estado_inicial),
            "aceptacion": sorted(self._n(e) for e in self.afn.estados_aceptacion),
            "transiciones": {
                self._n(estado): {
                    simbolo: [self._n(d) for d in destinos]
                    for simbolo, destinos in trans.items()
                    if destinos  # ← filtrar vacías
                }
                for estado, trans in self.afn.tabla_transiciones.items()
            }
        }

    def _info_afd(self, afd: AFD) -> dict:
        return {
            "nombre":     afd.nombre,
            "estados":    sorted(self._n(e) for e in afd.estados),
            "alfabeto":   sorted(afd.alfabeto),
            "inicial":    self._n(afd.estado_inicial),
            "aceptacion": sorted(self._n(e) for e in afd.estados_aceptacion),
            "transiciones": {
                self._n(estado): {
                    simbolo: self._n(destino)
                    for simbolo, destino in trans.items()
                }
                for estado, trans in afd.tabla_transiciones.items()
            }
        }

    def _traza_afn(self, cadena: str) -> list:
        estados_actuales = self.afn.cerradura_epsilon({self.afn.estado_inicial})
        traza = [{
            "paso":           0,
            "simbolo":        None,
            "estados_activos": sorted(self._n(e) for e in estados_actuales)
        }]

        for i, simbolo in enumerate(cadena, 1):
            estados_actuales = self.afn.cerradura_epsilon(
                self.afn.mover(estados_actuales, simbolo)
            )
            traza.append({
                "paso":           i,
                "simbolo":        simbolo,
                "estados_activos": sorted(self._n(e) for e in estados_actuales)
            })

        return traza

    def _resumen_minimizacion(self) -> dict:
        """
        Genera una explicación de estados que aparecen en el AFD
        pero desaparecen en el AFD mínimo.

        Solo informa; no altera la lógica de construcción/minimización.
        """
        solo_en_afd = sorted(set(self.afd.estados) - set(self.afd_min.estados))
        return {
            "cantidad_afd": len(self.afd.estados),
            "cantidad_afd_min": len(self.afd_min.estados),
            "cantidad_eliminados": len(solo_en_afd),
            "estados_eliminados": sorted(self._n(e) for e in solo_en_afd),
            "explicacion": (
                "Un estado puede existir en el AFD de subconjuntos y no aparecer "
                "en el AFD mínimo porque era equivalente a otro estado (indistinguible) "
                "o quedó absorbido durante el agrupamiento de minimización. "
                "Si además no tiene transiciones explícitas en la tabla, en este modelo "
                "eso se interpreta como transición implícita al estado trampa."
            ),
        }

    def validar(self, cadena: str) -> dict:
        return {
            "cadena": cadena,
            "valida": self.afd_min.validar(cadena)
        }

    def analizar(self, cadena: str) -> dict:
        return {
            "cadena":  cadena,
            "valida":  self.afd_min.validar(cadena),
            "afn":     self._info_afn(),
            "afd":     self._info_afd(self.afd),
            "afd_min": self._info_afd(self.afd_min),
            "minimizacion": self._resumen_minimizacion(),
            "traza":   self._traza_afn(cadena),
        }

    def __repr__(self) -> str:
        return (
            f"ServicioAutomata("
            f"afn={self.afn.nombre}, "
            f"afd={len(self.afd.estados)} estados, "
            f"min={len(self.afd_min.estados)} estados)"
        )
    def _mapear_nombres(self, estados: set) -> dict:
        """
        Mapea nombres internos de estados a nombres legibles.
        Ejemplo: '36_34_32_0_q0' → 'S0'
        """
        return {
            estado: f"S{i}"
            for i, estado in enumerate(sorted(estados))
        }