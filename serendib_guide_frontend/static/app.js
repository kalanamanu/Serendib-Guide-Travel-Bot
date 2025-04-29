document.addEventListener('DOMContentLoaded', function () {
    // Theme toggle functionality
    const themeToggle = document.getElementById('theme-toggle');
    const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)');

    // Check for saved theme preference or use system preference
    const currentTheme = localStorage.getItem('theme') ||
        (prefersDarkScheme.matches ? 'dark' : 'light');
    document.documentElement.setAttribute('data-theme', currentTheme);

    themeToggle.addEventListener('click', function () {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
    });

    // Chat functionality
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const chatMessages = document.getElementById('chat-messages');

    function addMessage(content, isUser) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;

        const avatarDiv = document.createElement('div');
        avatarDiv.className = 'avatar';
        const avatarIcon = document.createElement('i');
        avatarIcon.className = isUser ? 'fas fa-user' : 'fas fa-compass';
        avatarDiv.appendChild(avatarIcon);

        const contentDiv = document.createElement('div');
        contentDiv.className = 'content';
        const contentP = document.createElement('p');
        contentP.textContent = content;
        contentDiv.appendChild(contentP);

        messageDiv.appendChild(avatarDiv);
        messageDiv.appendChild(contentDiv);

        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function handleUserInput() {
        const message = userInput.value.trim();
        if (message) {
            // Hide initial greeting if it's still visible
            const initialGreeting = document.getElementById('initial-greeting');
            if (initialGreeting) {
                initialGreeting.classList.add('hidden');
            }

            addMessage(message, true);
            userInput.value = '';

            // Simulate bot response after a short delay
            setTimeout(() => {
                fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ message: message })
                })
                    .then(response => response.json())
                    .then(data => {
                        addMessage(data.response, false);
                    })
                    .catch(error => {
                        addMessage("Error connecting to server.", false);
                        console.error('Error:', error);
                    });
            }, 500);
        }
    }

    sendButton.addEventListener('click', handleUserInput);

    userInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            handleUserInput();
        }
    });

    // Focus input on load
    userInput.focus();
});