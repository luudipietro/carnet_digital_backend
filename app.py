from flask import Flask
from flask_cors import CORS
from extensions import db, ma, migrate
from api import bp as api_bp  # Importas tu Blueprint
import api.socios
import domain.deudas
import domain.socio
import os
from dotenv import load_dotenv
# Cargar las variables del archivo .env al inicio
load_dotenv()  # <--- ESTA LÍNEA ES CLAVE

def create_app():
    app = Flask(__name__)

    # 1. Configuración de la Base de Datos (Ejemplo con SQLite)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["JSON_AS_ASCII"] = False

    # 2. Inicializar extensiones con la app
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    CORS(app, resources={r"/api/*":{"origins":"*"}})

    # 3. Registrar el Blueprint de la API
    app.register_blueprint(api_bp)

    @app.get('/')
    def home():
        return 'API de socios de Mutual Sueño Amarillo'

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0')