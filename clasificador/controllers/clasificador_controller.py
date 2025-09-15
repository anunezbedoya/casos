from flask import Blueprint, request, jsonify
from clasificador.services.clasificador_service import clasificar_archivo
from clasificador.prompts.generador_prompt import generar_prompt

import requests

clasificador_bp = Blueprint('clasificador', __name__)

@clasificador_bp.route('/', methods=['POST'])
def clasificar():
    # 🔹 Recibir múltiples archivos
    archivos = request.files.getlist('archivos')
    url_cliente = request.form.get('url') or (request.json.get('url') if request.is_json else None)
    textos_concatenados = ""   # 👈 inicializamos

    funcion = 'clasificar'
    notificar_dispersion(url_cliente, funcion)

    if not archivos or len(archivos) == 0:
        return jsonify({'error': 'No se recibieron archivos'}), 400

    if not url_cliente:
        return jsonify({'error': 'URL del cliente no recibida'}), 400

    resultados = []
    for archivo in archivos:
        resultado = clasificar_archivo(archivo)
        textos_concatenados += f"\n\n{resultado}\n"

        resultados.append({
            "nombre_archivo": archivo.filename,
            "resultado": resultado
        })

    return generar_prompt(textos_concatenados)

def notificar_dispersion(url_cliente, funcion):
    data = {
        "url": url_cliente,
        "funcion": funcion
    }

    response = requests.post(
        "https://dispersion-718759852530.us-central1.run.app/dispersion",
        json=data
    )

    if response.status_code == 200:
        print("Registro en dispersión exitoso")
    else:
        print(f"Error en dispersión: {response.status_code} - {response.text}")