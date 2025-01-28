# __init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_cors import CORS
from config import DevelopmentConfig
from flask_migrate import Migrate

# Inicialización de extensiones
db = SQLAlchemy()
socketio = SocketIO()
migrate = None

def create_app():
    # Crear la instancia de la aplicación Flask
    app = Flask(__name__)

    # Configuración de la aplicación
    app.config.from_object(DevelopmentConfig)  # Cambiar según el entorno (Producción o Testing)

    # Inicializar la base de datos
    db.init_app(app)

    # Inicializar Flask-Migrate con la app y db
    global migrate
    migrate = Migrate(app, db)

    # Inicializar SocketIO
    socketio.init_app(app, cors_allowed_origins="*")

    # Configurar CORS
    CORS(app)  # Habilita CORS para toda la aplicación

    # Registrar las rutas usando un blueprint
    from .routes import bp as routes_blueprint
    app.register_blueprint(routes_blueprint)

    return app
