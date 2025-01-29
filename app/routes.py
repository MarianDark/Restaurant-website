from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from datetime import datetime
from .models import Menu, Reserva, Cliente
from . import db

# Crear instancia de Blueprint
bp = Blueprint('routes', __name__)

# Ruta principal
@bp.route('/')
def index():
    return redirect(url_for('routes.index_page'))

@bp.route('/index', methods=['GET'], endpoint='index_page')
def index_page():
    return render_template('index.html')

# Ruta para ver el menú
@bp.route('/menu', methods=['GET'], endpoint='menu')
def menu():
    comidas = Menu.query.filter_by(categoria='Comida').all()
    bebidas = Menu.query.filter_by(categoria='Bebida').all()
    postres = Menu.query.filter_by(categoria='Postre').all()
    return render_template('menu.html', comidas=comidas, bebidas=bebidas, postres=postres)

# Ruta para registrar un nuevo cliente
@bp.route('/register', methods=['GET', 'POST'], endpoint='register')
def register():
    if request.method == "POST":
        nombre = request.form['nombre']
        correo = request.form['correo']
        telefono = request.form['telefono']
        password = request.form['password']

        cliente_existente = Cliente.query.filter_by(correo=correo).first()
        if cliente_existente:
            flash("El correo ya está registrado.", "danger")
            return redirect(url_for('routes.register'))

        try:
            cliente = Cliente(nombre=nombre, correo=correo, telefono=telefono)
            cliente.set_password(password)
            db.session.add(cliente)
            db.session.commit()
        except ValueError as e:
            flash(f'Error: {e}', 'danger')
            return redirect(url_for('routes.register'))

        flash("Cuenta creada exitosamente, ¡inicia sesión!", "success")
        return redirect(url_for('routes.login'))

    return render_template("register.html")

# Ruta para iniciar sesión
@bp.route('/login', methods=['GET', 'POST'], endpoint='login')
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        password = request.form['password']
        cliente = Cliente.query.filter_by(correo=correo).first()

        if cliente and cliente.check_password(password):
            session['user_id'] = cliente.id
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('routes.index_page'))
        else:
            flash('Correo o contraseña incorrectos', 'danger')

    return render_template('login.html')

# Ruta para realizar una reserva
@bp.route('/reservar', methods=['GET', 'POST'], endpoint='reservar')
def reservar():
    if request.method == "POST":
        nombre_cliente = request.form['nombre']
        correo_cliente = request.form['correo']
        telefono_cliente = request.form['telefono']
        fecha_reserva = datetime.strptime(request.form['fecha'], "%Y-%m-%d").date()
        hora_reserva = datetime.strptime(request.form['hora'], "%H:%M").time()
        numero_personas = int(request.form['personas'])

        cliente = Cliente.query.filter_by(correo=correo_cliente).first()
        if not cliente:
            cliente = Cliente(nombre=nombre_cliente, correo=correo_cliente, telefono=telefono_cliente)
            cliente.set_password("default_password")
            db.session.add(cliente)
            db.session.commit()

        reserva = Reserva(
            fecha=fecha_reserva,
            hora=hora_reserva,
            numero_personas=numero_personas,
            cliente=cliente
        )
        db.session.add(reserva)
        db.session.commit()

        flash("Reserva realizada exitosamente!", "success")
        return redirect(url_for('routes.index_page'))

    return render_template("reservar.html")

# Ruta para ver reservas del usuario
@bp.route('/mis-reservas', methods=['GET'], endpoint='mis_reservas')
def mis_reservas():
    if 'user_id' not in session:
        flash("Por favor, inicia sesión para ver tus reservas.", "warning")
        return redirect(url_for('routes.login'))
    
    cliente = Cliente.query.get(session['user_id'])
    if not cliente:
        flash("No se encontró información del usuario.", "danger")
        return redirect(url_for('routes.index_page'))
    
    reservas = cliente.reservas
    return render_template('mis_reservas.html', reservas=reservas)

# Ruta para cerrar sesión
@bp.route('/logout', methods=['GET'], endpoint='logout')
def logout():
    session.pop('user_id', None)
    flash('Has cerrado sesión exitosamente.', 'success')
    return redirect(url_for('routes.index'))
