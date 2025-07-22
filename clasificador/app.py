from flask import Flask
from controllers.clasificador_controller import clasificador_bp

# Crear la aplicación Flask
app = Flask(__name__)

# Registrar el blueprint para el clasificador con el prefijo '/clasificar'
app.register_blueprint(clasificador_bp, url_prefix='/clasificar')