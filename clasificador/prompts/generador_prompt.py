import requests
import os
import json
import re

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def generar_prompt(texto):
    if not GEMINI_API_KEY:
        return {"error": "API key no configurada"}

    prompt = f"""Eres un experto en derecho colombiano y en análisis de documentos judiciales.  
Tu única tarea es identificar y clasificar demandas en Colombia.  

INSTRUCCIONES IMPORTANTES:  
- Responde únicamente con un JSON válido.  
- No repitas el rol, el contexto, ni la tarea.  
- No incluyas explicaciones, ni texto adicional fuera del JSON.  
- Escapa todas las comillas dobles internas como \\".  

TAREA:  
1. Determina si el documento es una DEMANDA u otro escrito judicial.  
2. Si es demanda, identifica y clasifica el **tipo de demanda** (ejemplo: "demanda laboral", "demanda civil de pertenencia", "demanda ejecutiva", "demanda penal", "demanda de nulidad", "acción de tutela", "demanda administrativa", etc.).  
3. Extrae los campos clave que justifiquen la clasificación.  

ENTRADA:
<<<
{texto[:3000]}
>>>

SALIDA (solo JSON válido):
{{
  "tipo_documento": "",
  "clasificacion": "",
  "tipo_demanda": "",
  "campos": {{
    "tipo_proceso": "",
    "partes_involucradas": "",
    "pretensiones": "",
    "hechos_relevantes": "",
    "normas_citadas": "",
    "juzgado_o_autoridad": "",
    "fecha_radicacion": "",
    "numero_radicado": "",
    "apoderados": "",
    "ciudad": ""
  }}
}}
"""

    # ✅ Aquí ya no retornamos, sino que llamamos al endpoint
    response = requests.post(
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent",
        params={"key": GEMINI_API_KEY},
        json={"contents": [{"parts": [{"text": prompt}]}]},
    )

    if response.status_code != 200:
        return {"error": response.text}

    result = response.json()
    text_result = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")

    # Limpieza del texto antes de parsear
    text_result = re.sub(r"```json|```", "", str(text_result)).strip()
    text_result = re.sub(r'(:\s*")([^"]*?)"([^"]*?")', r'\1\2\\\"\3', text_result)

    try:
        json_result = json.loads(text_result)

        # Si "contenido" es lista de diccionarios → unificar
        if isinstance(json_result.get("contenido"), list):
            contenido_unido = {}
            for item in json_result["contenido"]:
                if isinstance(item, dict):
                    contenido_unido.update(item)
            json_result["contenido"] = contenido_unido

        # 🔹 Limpieza final de barras invertidas sobrantes
        def limpiar_valores(data):
            if isinstance(data, dict):
                return {k: limpiar_valores(v) for k, v in data.items()}
            elif isinstance(data, list):
                return [limpiar_valores(v) for v in data]
            elif isinstance(data, str):
                return re.sub(r'\\+$', '', data).strip()
            return data

        json_result = limpiar_valores(json_result)
        return json_result

    except Exception as e:
        return {
            "error": f"No se pudo parsear la respuesta de Gemini: {e}",
            "respuesta_original": text_result
        }