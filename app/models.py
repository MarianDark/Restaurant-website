from datetime import datetime
import re
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

# Modelo para los clientes
class Cliente(db.Model):
    __tablename__ = 'clientes'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), nullable=False, unique=True)
    telefono = db.Column(db.String(15), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

# Relación con reservas
    reservas = db.relationship('Reserva', backref='cliente', lazy=True)

    def set_password(self, password):
        if not self.validar_contraseña(password):
            raise ValueError("La contraseña debe tener al menos 6 caracteres, incluyendo mayúsculas, minúsculas, números y caracteres especiales.")
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def validar_contraseña(self, password):
        patron = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[A-Z])(?=.*[!@#$%^&*(),.?":{}|<>])[A-Za-z\d!@#$%^&*(),.?":{}|<>]{6,}$'
        return bool(re.match(patron, password))

    def __repr__(self):
        return f'<Cliente {self.nombre}>'

# Modelo para las reservas
class Reserva(db.Model):
    __tablename__ = 'reservas'

    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)
    numero_personas = db.Column(db.Integer, nullable=False)

# Relación con clientes
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)

    def __repr__(self):
        return f'<Reserva {self.id}, Cliente {self.cliente.nombre}>'

# Modelo para el menú
class Menu(db.Model):
    __tablename__ = 'menu'

    id = db.Column(db.Integer, primary_key=True)
    categoria = db.Column(db.String(50), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(200), nullable=True)
    precio = db.Column(db.Float, nullable=False)
    puntuacion = db.Column(db.Float, default=0.0)
    imagen = db.Column(db.String(100))

    def actualizar_puntuacion(self, nueva_puntuacion):
        self.puntuacion = (self.puntuacion + nueva_puntuacion) / 2

    def __repr__(self):
        return f'<Menu {self.nombre}>'