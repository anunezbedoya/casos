import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask
from clasificador.controllers.clasificador_controller import clasificador_bp
app = Flask(__name__)
app.register_blueprint(clasificador_bp, url_prefix='/clasificar')



#port = int(os.environ.get('PORT', 8080))
#app.run(debug=True, host='0.0.0.0', port=port)
