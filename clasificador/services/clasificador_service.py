from clasificador.prompts.generador_prompt import generar_prompt
from pathlib import Path
from clasificador.utils.conversor_texto import extraer_texto_pdf
from clasificador.utils.conversor_texto import extraer_texto_imagen
from clasificador.utils.conversor_texto import extraer_texto_word
from clasificador.utils.conversor_texto import extraer_texto_excel



def clasificar_archivo(archivo) -> str:
    contenido = archivo.read()
    extension = Path(archivo.filename).suffix.lower()

    if extension == '.pdf':
        texto = extraer_texto_pdf(contenido)
        if len(texto.strip()) < 1000:
            texto_ocr = extraer_texto_imagen(contenido)
            if len(texto_ocr) > len(texto):
                texto = texto_ocr

    elif extension in ['.jpg', '.jpeg', '.png']:
        texto = extraer_texto_imagen(contenido)

    elif extension in ['.doc', '.docx']:
        texto = extraer_texto_word(contenido)

    elif extension in ['.xls', '.xlsx']:
        texto = extraer_texto_excel(contenido)

    else:
        return f"Tipo de archivo no soportado: {extension}"

    return generar_prompt(texto)
