from flask import Flask
from controllers.clasificador_controller import clasificador_bp
import os  
app = Flask(__name__)
app.register_blueprint(clasificador_bp, url_prefix='/clasificar')



#port = int(os.environ.get('PORT', 8080))
#app.run(debug=True, host='0.0.0.0', port=port)
