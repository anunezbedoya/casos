import requests
import os

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def generar_prompt(texto):
    if not GEMINI_API_KEY:
        return {"error": "API key no configurada"}

    #prompt = f"Clasifica el tipo de documento con base en el siguiente texto:\n\n{texto[:3000]} y entregame un array con los valores que puedas extraer"

    prompt =  f"""ROL: Experto en documentos públicos.

CONTEXTO: Eres un especialista con amplio conocimiento en todos los tipos de documentos que se utilizan en el ámbito gubernamental y empresarial de Colombia, tales como facturas, contratos, documentos de identidad, certificados, resoluciones, derechos de petición, PQRS, entre otros.

TAREA: Analiza el siguiente contenido en texto plano y responde con precisión qué tipo de documento es. Tu respuesta debe limitarse únicamente al tipo documental (por ejemplo: "factura", "contrato", "PQRS", "resolución", etc.). Además, extrae los campos clave que justifiquen esa clasificación, entregándolos como un arreglo de pares clave-valor.

Si identificas que el tipo de documento corresponde a alguno de los siguientes (factura, contrato o documento de identidad), asegúrate de extraer los datos clave correspondientes únicamente a ese tipo, con base en los campos definidos más abajo. Si no es posible extraer todos, incluye los que estén disponibles.

ENTRADA:
<<<
{texto[:3000]}
>>>

SALIDA ESPERADA (formato JSON):
{{
  "tipo_documento": "factura",
  "contenido": [
    {{ "numero_factura": "F-12456" }},
    {{ "fecha_emision": "2025-07-01" }},
    {{ "nombre_proveedor": "Empresa XYZ S.A.S." }},
    {{ "nit_proveedor": "900123456-7" }},
    {{ "total_pagar": "$5.600.000" }}
  ]
}}

CAMPOS CLAVE POR TIPO DOCUMENTAL:

FACTURA:
- Número de factura
- Fecha de emisión
- Fecha de vencimiento
- Nombre del proveedor
- NIT del proveedor
- Dirección del proveedor
- Nombre del cliente
- NIT del cliente
- Dirección del cliente
- Concepto o descripción del servicio/producto
- Cantidad
- Valor unitario
- Subtotal
- IVA
- Descuentos
- Total a pagar
- Forma de pago
- Estado de pago (pagada, pendiente, vencida)

CONTRATO:
- Tipo de contrato
- Empleador
- Valor mensual
- Fecha inicio
- Objeto del contrato
- Nombre empleado o contratista
- Persona jurídica o natural
- Valor del contrato

DOCUMENTO DE IDENTIDAD:
- Tipo de documento
- Número de documento
- Nombres
- Apellidos
- Fecha de nacimiento
- Lugar de nacimiento
- Nacionalidad
- Sexo
- Rh o grupo sanguíneo
- Fecha de expedición
- Lugar de expedición
- Entidad emisora
- Código MRZ (si aplica)
- Estado del documento (vigente, vencido, cancelado)
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