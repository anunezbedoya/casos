from flask import Blueprint, request, jsonify
from clasificador.services.clasificador_service import clasificar_archivo
from clasificador.prompts.generador_prompt import generar_prompt, generar_resumenes
import traceback
import requests

clasificador_bp = Blueprint('clasificador', __name__)

@clasificador_bp.route('/', methods=['POST'])
def clasificar():

    try:
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
            try:
                texto_extraido = clasificar_archivo(archivo)
                documentos[archivo.filename] = texto_extraido
            except Exception as e:
                print(f"⚠️ Error extrayendo texto de {archivo.filename}: {e}")
                continue
        if not documentos:
            return jsonify({'error': 'No se pudo procesar ningún archivo válido'}),400

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
        
        if "error" in resultado_final:
            return jsonify({
                "error": "Ocurrió un problema con el modelo de IA",
                "detalle": resultado_final["error"]
            }),502

        return jsonify(resultado_final),200
    
    except Exception as e:
        print("❌ ERROR INTERNO DEL SERVIDOR ❌")
        traceback.print_exc()

        return jsonify({
            "error": "Error interno del servidor",
            "detalle": str(e)
        }), 500

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