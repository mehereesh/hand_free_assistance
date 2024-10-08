const startBtn = document.getElementById('start-btn');
const stopBtn = document.getElementById('stop-btn');
const statusText = document.getElementById('status');

const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.continuous = true;
recognition.lang = 'en-US';

recognition.onstart = function() {
    statusText.textContent = 'Listening...';
};

recognition.onresult = function(event) {
    const transcript = event.results[event.resultIndex][0].transcript.trim().toLowerCase();
    statusText.textContent = `Heard: ${transcript}`;
    executeCommand(transcript);
};

recognition.onend = function() {
    statusText.textContent = 'Click "Start Listening" to begin.';
};

recognition.onerror = function(event) {
    statusText.textContent = `Error occurred in recognition: ${event.error}`;
};

startBtn.addEventListener('click', () => {
    recognition.start();
});

stopBtn.addEventListener('click', () => {
    recognition.stop();
    statusText.textContent = 'Stopped listening.';
});

function executeCommand(command) {
    console.log(`Sending command: ${command}`);  // Debug information
    fetch('/command', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ command: command })
    })
    .then(response => response.json())
    .then(data => {
        const response = data.response;
        statusText.textContent = response;
        console.log(`Received response: ${response}`);  // Debug information
        speak(response);
    })
    .catch(error => {
        console.error('Error:', error);  // Debug information
        statusText.textContent = 'Error occurred. Check console for details.';
    });
}

function speak(text) {
    const utterance = new SpeechSynthesisUtterance(text);
    window.speechSynthesis.speak(utterance);
}
