function startGame() {
    const request = new XMLHttpRequest();
    const startPath = '/startGame'
    const startButton = document.getElementById('startButton').onclick

    const startState = function () {
        request.open('GET', startPath);
        request.send();
    };
}