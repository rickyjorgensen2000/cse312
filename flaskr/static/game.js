// Handle in game actions...
// Buttons will be linked to this file

const socket = new WebSocket('ws://' + window.location.host + '/websocket');

let webRTCConnection;
let player = '';
let state = 0;
// Wait to establish websocket connection
socket.onopen = function (e) {
    alert('Connection Established')
    socket.send('Ready to Tic Tac Toe')
}

// Handle message from server
socket.onmessage = function (ws_message) {
    const message = JSON.parse(ws_message.data);
    const messageType = message.messageType
    // assign player as 'X' or 'O'
    // assign the current state to determine who's move it is
    player = message['state'];
    if (player === 'X'){
        state = 1;
    }
    console.log("reached js")
}

// Event Handler for clicking game board
function triggerButton (buttonID) {
    if (state) {
        let button = document.getElementById(buttonID);
        if (player === 'X') {
            button.style.opacity = '1';
            button.innerText = 'X';
        }
        if (player === 'O') {
            button.innerText = 'O';
        }
        button.style.visibility = 'visible'
        state = 0;

    }
}