from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_cors import CORS
from flask_migrate import Migrate
from config import DevelopmentConfig  # Cambia esto según tu configuración

# Inicialización de extensiones
db = SQLAlchemy()
socketio = SocketIO()
migrate = None

def create_app():
    # Crear la instancia de la aplicación Flask
    app = Flask(__name__)

    # Configuración de la aplicación
    app.config.from_object(DevelopmentConfig)  # Cambiar según el entorno (Producción o Testing)

    # Configurar la carpeta estática (aunque por defecto Flask ya maneja esto)
    app.config['STATIC_FOLDER'] = 'static'

    # Configuración de la base de datos
    db.init_app(app)

    # Inicializar Flask-Migrate con la app y db
    global migrate
    migrate = Migrate(app, db)

    # Inicializar SocketIO
    socketio.init_app(app, cors_allowed_origins="*")

    # Configurar CORS para permitir solicitudes de diferentes orígenes
    CORS(app)  # Habilita CORS para toda la aplicación

    # Registrar las rutas usando un blueprint (aquí puedes modularizar las rutas)
    from .routes import bp as routes_blueprint
    app.register_blueprint(routes_blueprint)

    return app
