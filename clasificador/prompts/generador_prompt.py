import requests
import os

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def generar_prompt(texto):
    if not GEMINI_API_KEY:
        return {"error": "API key no configurada"}

    #prompt = f"Clasifica el tipo de documento con base en el siguiente texto:\n\n{texto[:3000]} y entregame un array con los valores que puedas extraer"

    prompt = prompt = f"""
ROL: Experto en documentos públicos.

CONTEXTO: Eres un especialista con amplio conocimiento en todos los tipos de documentos que se utilizan en el ámbito gubernamental y empresarial de Colombia, tales como facturas, contratos, documentos de identidad, certificados, resoluciones, derechos de petición, PQRS, entre otros.

TAREA: Analiza el siguiente contenido en texto plano y responde con precisión qué tipo de documento es. Tu respuesta debe limitarse únicamente al tipo documental (por ejemplo: "factura", "contrato", "PQRS", "resolución", etc.). Además, extrae los campos clave que justifiquen esa clasificación, entregándolos como un arreglo de pares clave-valor.

ENTRADA:
<<<
{texto[:3000]}
>>>

SALIDA ESPERADA (JSON):
{{
  "tipo_documento": "factura",
  "contenido": [
    {{ "fecha_emision": "2025-07-01" }},
    {{ "numero_factura": "F-12456" }},
    {{ "nit_emisor": "900123456-7" }},
    {{ "razon_social": "Empresa XYZ S.A.S." }},
    {{ "valor_total": "$5.600.000" }}
  ]
}}
"""


    response = requests.post(
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent",
        params={"key": GEMINI_API_KEY},
        json={
            "contents": [{"parts": [{"text": prompt}]}]
        },
    )

    if response.status_code != 200:
        return {"error": response.text}

    result = response.json()
    return result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", result)