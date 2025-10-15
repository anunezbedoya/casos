from pathlib import Path
from clasificador.utils.conversor_texto import (
    extraer_texto_pdf,
    extraer_texto_pdf_ocr,
    extraer_texto_imagen,
    extraer_texto_word,
    extraer_texto_excel
)
from clasificador.prompts.generador_prompt import generar_prompt

EXTENSIONES_SOPORTADAS = ['.pdf', '.jpg', '.jpeg', '.png', '.doc', '.docx', '.xls', '.xlsx']
MIMES_SOPORTADAS = [
    'application/pdf',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/msword',
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'image/png',
    'image/jpeg'
]

def archivo_permitido(filename: str, mimetype: str) -> bool:
    """Valida extension y tipo MIME del archivo."""
    ext = Path(filename).suffix.lower()
    return ext in EXTENSIONES_SOPORTADAS and mimetype in MIMES_SOPORTADAS

def clasificar_archivo(archivo) -> str:
    try:
        contenido = archivo.read()
        extension = Path(archivo.filename).suffix.lower()

        if extension not in EXTENSIONES_SOPORTADAS:
            return f"Tipo de archivo no soportado: {extension}"

        texto = ""

        if extension == '.pdf':
            texto = extraer_texto_pdf(contenido)
            if len(texto.strip()) < 1000:
                texto_ocr = extraer_texto_pdf_ocr(contenido)
                if len(texto_ocr) > len(texto):
                    texto = texto_ocr

        elif extension in ['.jpg', '.jpeg', '.png']:
            texto = extraer_texto_imagen(contenido)

        elif extension in ['.doc', '.docx']:
            texto = extraer_texto_word(contenido)

        elif extension in ['.xls', '.xlsx']:
            texto = extraer_texto_excel(contenido)

        if not texto.strip():
            return "No se pudo extraer texto del archivo."

        return texto

    except Exception as e:
        return f"Error procesando el archivo: {str(e)}"