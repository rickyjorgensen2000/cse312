// Handle in game actions...
// Buttons will be linked to this file


const socket = new WebSocket('ws://' + window.location.host);

let webRTCConnection;
let player = '';
let state = 0;
let myMoves = [];
let oppMoves = [];
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
    if(messageType === 'assignPlayer') {
        player = message['state'];
        if (player === 'X') {
            state = 1;
        }
    }
    else if (messageType === 'move'){
        update_opponent_move(message['buttonID'])
    }
    console.log("reached js")
}

// Event Handler for clicking game board
function triggerButton (buttonID) {
    if (state) {
        let button = document.getElementById(buttonID);
        myMoves.push(buttonID)
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

function update_opponent_move (buttonID) {
    let button = document.getElementById(buttonID);
    oppMoves.push(buttonID)
    switch (player) {
        case 'X':
            button.style.opacity = '1';
            button.innerText = 'O';
            break
        case 'O':
            button.style.opacity = '1';
            button.innerText = 'X';
            break
    }
    state = 1;
}
// check if a player has won
function check_game_state(myMoves, oppMoves) {

}