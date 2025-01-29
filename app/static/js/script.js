// Conectar al servidor Socket.IO
const socket = io();  // Se asegura de que el cliente esté configurado correctamente

// Detectar conexión exitosa
socket.on('connect', () => {
    console.log('Conectado al servidor Socket.IO');
});

// Escuchar mensajes del servidor y agregarlos a la vista
socket.on('message', function (msg) {
    const messageDiv = document.getElementById('messages');
    if (messageDiv) {
        const newMessage = document.createElement('p');
        newMessage.textContent = msg;
        messageDiv.appendChild(newMessage);
    } else {
        console.warn('El contenedor de mensajes no fue encontrado.');
    }
});

// Enviar mensaje al servidor
function sendMessage() {
    const messageInput = document.getElementById('message');
    if (messageInput) {
        const message = messageInput.value.trim();
        if (message) {
            socket.send(message);
            messageInput.value = ''; // Vaciar el campo de entrada después de enviar
        } else {
            alert('Por favor escribe un mensaje antes de enviarlo.');
        }
    } else {
        console.warn('El campo de entrada de mensajes no fue encontrado.');
    }
}

// Banner index: Carrusel de imágenes
document.addEventListener("DOMContentLoaded", function () {
    let currentIndex = 0;
    const images = document.querySelectorAll('.banner-image');
    const totalImages = images.length;
    const bannerContainer = document.querySelector('.banner-images');

    if (images.length > 0 && bannerContainer) {
        function changeImage() {
            currentIndex = (currentIndex + 1) % totalImages;
            bannerContainer.style.transform = `translateX(-${currentIndex * 100}%)`;
        }

        // Cambia de imagen cada 4 segundos (4000 milisegundos)
        setInterval(changeImage, 4000);
    } else {
        console.warn("No se encontraron imágenes en el banner.");
    }
});

// Carrusel de publicidad
document.addEventListener("DOMContentLoaded", function () {
    let index = 0;
    const ads = document.querySelectorAll(".carousel a");
    const totalAds = ads.length;

    if (totalAds > 0) {
        function showNextAd() {
            ads.forEach(ad => ad.style.display = "none");
            ads[index].style.display = "block";
            index = (index + 1) % totalAds;
        }

        showNextAd();
        setInterval(showNextAd, 5000);
    } else {
        console.warn("No se encontraron anuncios en el carrusel de publicidad.");
    }
});

// Manejo de navegación de los botones de autenticación
document.addEventListener("click", function(event) {
    if (event.target.matches(".auth-buttons .btn")) {
        console.log("Botón de autenticación clickeado:", event.target.href);
        window.location.href = event.target.href;
    }
});
