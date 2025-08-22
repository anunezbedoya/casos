import requests
import os
import json
import re

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def generar_prompt(texto):
    if not GEMINI_API_KEY:
        return {"error": "API key no configurada"}

    prompt = f"""ROL: Experto en documentos públicos.

CONTEXTO: Eres un especialista con amplio conocimiento en todos los tipos de documentos que se utilizan en el ámbito gubernamental y empresarial de Colombia, tales como facturas, contratos, documentos de identidad, certificados, resoluciones, derechos de petición, PQRS, entre otros.

TAREA: Analiza el siguiente contenido en texto plano y responde con precisión qué tipo de documento es. Tu respuesta debe limitarse únicamente al tipo documental (por ejemplo: "factura", "contrato", "PQRS", "resolución", etc.). Además, extrae los campos clave que justifiquen esa clasificación, entregándolos como un arreglo de pares clave-valor.

Si identificas que el tipo de documento corresponde a alguno de los siguientes (factura, contrato o documento de identidad), asegúrate de extraer los datos clave correspondientes únicamente a ese tipo, con base en los campos definidos más abajo. Si no es posible extraer todos, incluye los que estén disponibles.

ENTRADA:
<<<
{texto[:3000]}
>>>

SALIDA ESPERADA:
- Formato JSON válido (sin ``` ni lenguaje).
- Escapa todas las comillas dobles internas como \\".
- No incluyas texto adicional fuera del JSON.

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

CONTRATO LABORAL:
- Tipo de contrato
- Empleador
- Valor mensual
- Fecha inicio
- Objeto del contrato
- Nombre empleado o contratista
- Persona jurídica o natural
- Valor del contrato
- Tipo de persona (Natural-Jurídica)
- Tipo de documento (NIT, Pasaporte, Cédula)
- Número de identificación o NIT
- Dígito de verificación (si es jurídica)
- Razón social (si es jurídica)
- Primer nombre
- Segundo nombre
- Primer apellido
- Segundo apellido
- Correo
- Teléfono
- Dirección
- País
- Departamento
- Ciudad
- Número de contrato
- Valor base del contrato
- IVA (si aplica)
- Impuesto de consumo (si aplica)

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
        json={"contents": [{"parts": [{"text": prompt}]}]},
    )

    if response.status_code != 200:
        return {"error": response.text}

    result = response.json()
    text_result = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", result)

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

        # 🔹 Limpieza final de barras invertidas sobrantes al final
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