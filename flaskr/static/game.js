let state = 0
let player = ''
let myMoves = [];
let oppMoves = [];


function set_state(value) {
    state = value;
}


function set_player(value) {
    player = value;
}

// Event Handler for clicking game board
function triggerButton (buttonID, socket) {
    let button = document.getElementById(buttonID);
    console.log(button.innerText)
    if (state && (button.innerText !== 'X' && button.innerText !== 'O')) {
        myMoves.push(buttonID)
        if (player === 'X') {
            button.style.opacity = '1';
            button.innerText = 'X';
            socket.emit('player move', {'ButtonID': buttonID})
        }
        if (player === 'O') {
            button.style.opacity = '1';
            button.innerText = 'O';
            socket.emit('player move', {'ButtonID': buttonID})
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
    set_state(1);
}
// check if a player has won
function check_game_state(myMoves, oppMoves) {

}