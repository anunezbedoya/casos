from clasificador.utils.conversor_texto import convertir_a_texto
from prompts.generador_prompt import generar_prompt

def clasificar_archivo(archivo):
    texto = convertir_a_texto(archivo)
    return generar_prompt(texto)