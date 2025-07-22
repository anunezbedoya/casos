from flask import Blueprint, request, jsonify
from clasificador.services.clasificador_service import clasificar_archivo

clasificador_bp = Blueprint('clasificador', __name__)

@clasificador_bp.route('/', methods=['POST'])
def clasificar():
    archivo = request.files.get('archivo')
    if not archivo:
        return jsonify({'error': 'Archivo no recibido'}), 400
    
    resultado = clasificar_archivo(archivo)
    return jsonify({'resultado': resultado})