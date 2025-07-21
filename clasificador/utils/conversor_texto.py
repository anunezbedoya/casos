def convertir_a_texto(archivo):
    contenido = archivo.read()
    try:
        return contenido.decode('utf-8')
    except UnicodeDecodeError:
        return contenido.decode('latin-1')