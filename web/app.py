from flask import Flask, render_template, request

from Dominio_automatas.validadores.ipv4 import construir_afn_ipv4
from servicios.servicio_automata import ServicioAutomata

app = Flask(__name__)
servicio_ipv4 = ServicioAutomata(construir_afn_ipv4())


@app.get("/")
def inicio():
    return render_template(
        "index.html",
        cadena="",
        resultado=None,
        analisis=None,
    )


@app.post("/validar")
def validar_ipv4():
    cadena = request.form.get("cadena", "").strip()
    analisis = servicio_ipv4.analizar(cadena)
    return render_template(
        "index.html",
        cadena=cadena,
        resultado=analisis["valida"],
        analisis=analisis,
    )


@app.get("/api/validar")
def api_validar_ipv4():
    cadena = request.args.get("cadena", "").strip()
    return servicio_ipv4.validar(cadena)
