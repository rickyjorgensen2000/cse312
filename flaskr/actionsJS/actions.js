function startGame() {
    const request = new XMLHttpRequest();
    const startPath = '/startGame'
    request.open('GET', startPath);
    request.send();
}
// called when user clicks login button
function login() {
    const request = new XMLHttpRequest()
    let username = document.getElementById('login-box');
    username.focus();
    const nextPath = '/'
    request.open('POST', nextPath);
    request.send();
}


