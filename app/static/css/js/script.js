// Establish connection to the server using Socket.IO
var socket = io();

// Listen to messages from the server
socket.on('message', function (msg) {
    var messageDiv = document.getElementById('messages');
    if (messageDiv) {
        var newMessage = document.createElement('p');
        newMessage.textContent = msg;
        messageDiv.appendChild(newMessage);
    } else {
        console.error('The message container was not found.');
    }
});

// Send message to server
function sendMessage() {
    var messageInput = document.getElementById('message');
    if (messageInput) {
        var message = messageInput.value.trim();
        if (message) {
            socket.send(message);
            messageInput.value = ''; // Empty input after sending
        } else {
            alert('Please write a message before sending it.');
        }
    } else {
        console.error('The message input field was not found.');
    }
}
