from flask import Blueprint, request, jsonify
from clasificador.services.clasificador_service import clasificar_archivo
from clasificador.prompts.generador_prompt import generar_prompt, generar_resumenes

import requests

clasificador_bp = Blueprint('clasificador', __name__)

@clasificador_bp.route('/', methods=['POST'])
def clasificar():
    # 🔹 Recibir múltiples archivos
    archivos = request.files.getlist('archivos')
    url_cliente = request.form.get('url') or (request.json.get('url') if request.is_json else None)


    funcion = 'clasificar'
    notificar_dispersion(url_cliente, funcion)

    if not archivos or len(archivos) == 0:
        return jsonify({'error': 'No se recibieron archivos'}), 400

    if not url_cliente:
        return jsonify({'error': 'URL del cliente no recibida'}), 400

    documentos = {}     
    for archivo in archivos:
        texto_extraido = clasificar_archivo(archivo)
        documentos[archivo.filename] = texto_extraido

    if len(documentos) == 1:
        # Solo un archivo → análisis directo
        nombre, texto = list(documentos.items())[0]
        print(f"📄 Análisis directo para: {nombre}")
        resultado_final = generar_prompt([{
            "documento": nombre,
            "resumen": texto,
            "tipo_documento": "Desconocido",
            "indicadores_clave": {}
        }])
    else:
        # Varios archivos → flujo normal (resúmenes + análisis final)
        resumenes = generar_resumenes(documentos)
        resultado_final = generar_prompt(resumenes)

    return jsonify(resultado_final)

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