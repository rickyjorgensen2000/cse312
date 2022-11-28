// Handle in game actions...
// Buttons will be linked to this file

const socket = new WebSocket('ws://' + window.location.host + '/websocket');

let webRTCConnection;
let player = 'X';
socket.onmessage = function (ws_message) {
    const message = JSON.parse(ws_message.data);
    const messageType = message.messageType
    console.log("reached js")


}

function triggerButton (buttonID) {
    let button = document.getElementById(buttonID);
    if (player === 'X') {
        button.innerText = 'X';
    }
    if (player === 'O') {
        button.innerText = 'O';
    }
    button.style.visibility = 'visible'
}