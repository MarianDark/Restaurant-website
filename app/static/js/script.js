// Conectar al servidor Socket.IO
const socket = io();  // Esto funcionará una vez que el cliente esté configurado correctamente

// Ejemplo: Detectar conexión exitosa
socket.on('connect', () => {
    console.log('Conectado al servidor Socket.IO');
});

// Escuchar mensajes del servidor
socket.on('message', function (msg) {
    var messageDiv = document.getElementById('messages');
    if (messageDiv) {
        var newMessage = document.createElement('p');
        newMessage.textContent = msg;
        messageDiv.appendChild(newMessage);
    } else {
        console.error('El contenedor de mensajes no fue encontrado.');
    }
});

// Enviar mensaje al servidor
function sendMessage() {
    var messageInput = document.getElementById('message');
    if (messageInput) {
        var message = messageInput.value.trim();
        if (message) {
            socket.send(message);
            messageInput.value = ''; // Vaciar el campo de entrada después de enviar
        } else {
            alert('Por favor escribe un mensaje antes de enviarlo.');
        }
    } else {
        console.error('El campo de entrada de mensajes no fue encontrado.');
    }
}

// Banner index: Carrusel de imágenes
let currentIndex = 0;
const images = document.querySelectorAll('.banner-image');
const totalImages = images.length;

function changeImage() {
    // Incrementa el índice o reinícialo cuando supere la cantidad de imágenes
    currentIndex = (currentIndex + 1) % totalImages;

    // Mueve el contenedor de imágenes a la posición correcta
    document.querySelector('.banner-images').style.transform = `translateX(-${currentIndex * 100}%)`;
}

// Cambia de imagen cada 3 segundos (3000 milisegundos)
setInterval(changeImage, 4000);
