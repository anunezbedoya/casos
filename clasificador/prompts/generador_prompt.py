def generar_prompt(texto):
    if "factura" in texto.lower():
        return "Factura"
    elif "contrato" in texto.lower():
        return "Contrato"
    else:
        return "Documento genérico"