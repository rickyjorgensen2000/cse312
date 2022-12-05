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
    if (state && (button.innerText !== 'X' && button.innerText !== 'O')) {
        myMoves.push(parseInt(buttonID))
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
        if (check_game_state(oppMoves)) {
            socket.omit('win',{'player': player})
    }
        set_state(0);

    }
}

function update_opponent_move (buttonID) {
    let button = document.getElementById(buttonID);
    oppMoves.push(parseInt(buttonID))
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
    // check if the opponent won with last move
    if (check_game_state(oppMoves)) {
        set_state(0);
        let otherPlayer;
        if (player === 'X'){
            otherPlayer = 'O';
        }
        else {
            otherPlayer = 'X';
        }
        socket.omit('win',{'player': otherPlayer})
    }
    else{
        set_state(1);
    }
}
// check if a player has won
function check_game_state(moves) {
        const winConditions = [
            [1, 2, 3],
            [1, 5, 9],
            [1, 4, 7],
            [4, 5, 6],
            [2, 5, 8],
            [7, 8, 9],
            [3, 6, 9],
            [3, 5, 7]
        ];
        let win = false
        for (let condition in winConditions) {
            let count = 0;
            for (let move in condition) {
                if (moves.prototype.includes(move)) {
                    count++;
                }
                else {
                    break;
                }
            }
            if (count === 3) {
                win = true;
                break
            }
        }
        return win
}