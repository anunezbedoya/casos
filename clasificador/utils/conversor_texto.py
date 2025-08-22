from PyPDF2 import PdfReader
from docx import Document
import pandas as pd
import pytesseract
from PIL import Image
import io

from pdf2image import convert_from_bytes


def extraer_texto_pdf(file_bytes):
    # Intentar extracción por texto (PDF no escaneado)
    try:
        from PyPDF2 import PdfReader
        reader = PdfReader(io.BytesIO(file_bytes))
        texto = "".join([page.extract_text() or "" for page in reader.pages])
        return texto
    except Exception as e:
        return ""

def extraer_texto_pdf_ocr(file_bytes):
    # OCR de PDF escaneado
    pages = convert_from_bytes(file_bytes)
    texto_total = ""
    for page in pages:
        texto_total += pytesseract.image_to_string(page, lang="spa")
    return texto_total



def extraer_texto_imagen(file_bytes):
    image = Image.open(io.BytesIO(file_bytes))
    return pytesseract.image_to_string(image, lang="spa")

def extraer_texto_word(file_bytes):
    """Extrae texto de un archivo Word (.docx) dado como bytes."""
    doc = Document(io.BytesIO(file_bytes))
    return "\n".join([p.text for p in doc.paragraphs])

def extraer_texto_excel(file_bytes):
    """Extrae texto de un archivo Excel (.xls, .xlsx) dado como bytes."""
    try:
        xls = pd.read_excel(io.BytesIO(file_bytes), sheet_name=None)
        contenido = ""
        for nombre, hoja in xls.items():
            contenido += f"--- Hoja: {nombre} ---\n"
            contenido += hoja.to_string(index=False)
        return contenido
    except Exception as e:
        return f"Error leyendo Excel: {e}"
