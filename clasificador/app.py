from flask import Flask
from controllers.clasificador_controller import clasificador_bp

app = Flask(__name__)
app.register_blueprint(clasificador_bp, url_prefix='/clasificar')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8082)