function startGame() {
    const request = new XMLHttpRequest();
    const startPath = '/startGame'
    request.open('GET', startPath);
    request.send();
}

function login() {
    const request = new XMLHttpRequest()
    const nextPath = '/home'
    request.open('GET', nextPath);
    request.send();
}

