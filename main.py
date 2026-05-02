from Dominio_automatas.automatas.octeto import construir_afn_octeto
from Dominio_automatas.automatas.separador_ipv4 import construir_afn_punto
from Dominio_automatas.operaciones.concatenar import concatenar
from Dominio_automatas.operaciones.repetir import repetir
from Dominio_automatas.operaciones.minimizar import minimizar
from Dominio_automatas.operaciones.subconjuntos import afn_a_afd
from servicios.servicio_automata import ServicioAutomata
from Dominio_automatas.validadores.ipv4 import construir_afn_ipv4
import json





def main():
    print("=" * 40)
    print("AFN Octeto IPv4")
    print("=" * 40)
    
    afn_octeto = construir_afn_octeto()
    
    casos_octeto = [
        ("01",   False), # No se permiten ceros a la izquierda
        ("000",  False), # No se permite más de  un dígito si el número es 0
        ("0",    True),
        ("9",    True),
        ("42",   True),
        ("99",   True),
        ("100",  True),
        ("150",  True),
        ("199",  True),
        ("200",  True),
        ("248",  True),
        ("253",  True),
        ("255",  True),
        ("256",  False),
        ("300",  False),
        ("999",  False),
        ("01",   False),
        ("",     False),
        ("12a",  False),
    ]
    
    for cadena, esperado in casos_octeto:
        resultado = afn_octeto.validar(cadena)
        estado = "✅" if resultado == esperado else "❌"
        print(f"{estado} '{cadena}' → {'Aceptada' if resultado else 'Rechazada'} (esperado: {'Aceptada' if esperado else 'Rechazada'})")

    print()
    print("=" * 40)
    print("AFN Separador IPv4")
    print("=" * 40)

    afn_punto = construir_afn_punto()

    casos_punto = [
        (".",  True),
        ("",   False),
        (",",  False),
        (":",  False),
        ("..", False),
    ]

    for cadena, esperado in casos_punto:
        resultado = afn_punto.validar(cadena)
        estado = "✅" if resultado == esperado else "❌"
        print(f"{estado} '{cadena}' → {'Aceptada' if resultado else 'Rechazada'} (esperado: {'Aceptada' if esperado else 'Rechazada'})")

    afn_oct_punto = concatenar(afn_octeto, afn_punto)

    casos_concat = [
        ("192.", True),
        ("0.",   True),
        ("255.", True),
        ("256.", False),
        ("192",  False),
        (".",    False),
    ]

    print("=" * 40)
    print("AFN Octeto + Punto")
    print("=" * 40)

    for cadena, esperado in casos_concat:
        resultado = afn_oct_punto.validar(cadena)
        estado = "✅" if resultado == esperado else "❌"
        print(f"{estado} '{cadena}' → {'Aceptada' if resultado else 'Rechazada'} (esperado: {'Aceptada' if esperado else 'Rechazada'})")


    afn_punto  = construir_afn_punto()
    afn_octeto = construir_afn_octeto()
    afn_ipv4   = repetir(afn_octeto, n=4, separador=afn_punto)

    casos_ipv4 = [
        ("192.168.1.1",   True),
        ("0.0.0.0",       True),
        ("255.255.255.255",True),
        ("192.168.1.256", False),
        ("192.168.1.",    False),
        ("192.168.1",     False),
        ("192.168.1.1.1", False),
        ("",              False),
    ]

    print("=" * 40)
    print("AFN IPv4")
    print("=" * 40)
    afn_ipv4 = repetir(afn_octeto, n=4, separador=afn_punto)
    print(f"afn_ipv4: {afn_ipv4}")
    print(f"afn_octeto: {afn_octeto}")
    print(f"afn_punto: {afn_punto}")

    for cadena, esperado in casos_ipv4:
        resultado = afn_ipv4.validar(cadena)
        estado = "✅" if resultado == esperado else "❌"
        print(f"{estado} '{cadena}' → {'Aceptada' if resultado else 'Rechazada'} (esperado: {'Aceptada' if esperado else 'Rechazada'})")

    afd_ipv4     = afn_a_afd(afn_ipv4)
    afd_ipv4_min = minimizar(afd_ipv4)

    print(f"\nAFD IPv4:          {afd_ipv4}")
    print(f"AFD IPv4 mínimo:   {afd_ipv4_min}")
    print("\nValidando con AFD mínimo:")

    for cadena, esperado in casos_ipv4:
        resultado = afd_ipv4_min.validar(cadena)
        estado = "✅" if resultado == esperado else "❌"
        print(f"{estado} '{cadena}' → {'Aceptada' if resultado else 'Rechazada'}")

    servicio = ServicioAutomata(construir_afn_ipv4())
    print(servicio.validar("192.168.1.1"))
    print(servicio.validar("300.1.1.1"))
    resultado = servicio.analizar("192.168.1.1")
    print(json.dumps(resultado, indent=2, ensure_ascii=False))
            
if __name__ == "__main__":
    main()