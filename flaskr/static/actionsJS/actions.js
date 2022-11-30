function startGame() {
    const request = new XMLHttpRequest();
    const startPath = '/startGame'
    request.open('GET', startPath);
    request.send();
}
// called when user clicks login button
// take the input username send to server, if exist proceed to main
// if username does not exist prompt user to create one
function login() {
    const request = new XMLHttpRequest()
    let username = document.getElementById('login-box');
    username.focus();
    const nextPath = '/'
    request.open('POST', nextPath);
    request.send();
}

// Event handler for when user clicks leaderboard button
function getLeaderboard() {

}



function login1() {
    const request = new XMLHttpRequest()
    const nextPath = '/home'
    request.open('GET', nextPath);
    request.send();
}

