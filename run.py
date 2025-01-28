from app import create_app, socketio

# Crear la instancia de la aplicación Flask
app = create_app()

if __name__ == '__main__':
    try:
        # Ejecutar la aplicación con SocketIO en el puerto 5000
        socketio.run(app, host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")