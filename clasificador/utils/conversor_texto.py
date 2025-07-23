from PyPDF2 import PdfReader
from docx import Document
import pandas as pd
import pytesseract
from PIL import Image
import io

def extraer_texto_pdf(file_bytes):
    """Extrae texto de un archivo PDF dado como bytes."""
    stream = io.BytesIO(file_bytes)
    reader = PdfReader(stream)
    texto = ""
    for page in reader.pages:
        texto += page.extract_text() or ""
    return texto.strip()

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

def extraer_texto_imagen(file_bytes):
    """Extrae texto de una imagen (JPG, PNG) usando OCR."""
    image = Image.open(io.BytesIO(file_bytes))
    return pytesseract.image_to_string(image)