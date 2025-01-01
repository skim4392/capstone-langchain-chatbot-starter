function sendMessage() {
    clearError();

    let sendButton = document.getElementById('send-btn');
    let messageInput = document.getElementById('message-input');
    let message = messageInput.value;

    if (message === "") {
        displayError('Please type a message so I can assist you!');
        return;
    }

    displayMessage('user', message)
    
    // Get the selected function from the dropdown menu
    let functionSelect = document.getElementById('function-select');
    let selectedFunction = functionSelect.value;
    
    // Send an AJAX request to the Flask API endpoint based on the selected function
    let xhr = new XMLHttpRequest();
    let url;

    switch (selectedFunction) {
        case 'search':
            url = '/search';
            break;
        case 'kbanswer':
            url = '/kbanswer';
            break;
        case 'answer':
            url = '/answer';
            break;
        default:
            url = '/answer';
    }
    
    xhr.open('POST', url);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.addEventListener('loadstart', function() {
        sendButton.setAttribute('disabled', true);
        let spinner = document.createElement('i');
        spinner.classList.add('fa-md', 'fa-solid', 'fa-spinner', 'fa-spin-pulse');

        let loader = document.createElement('div');
        let text = document.createElement('span');
        text.classList.add('ml-1', 'loading-text');
        text.innerText = 'Thinking...';
        loader.appendChild(spinner);
        loader.appendChild(text);
        loader.id = 'loading-spinner';

        let chatContainer = document.getElementById('chat-container');
        chatContainer.appendChild(loader);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    });
    xhr.addEventListener('loadend', function() {
        sendButton.removeAttribute('disabled');
        let spinner = document.getElementById('loading-spinner');
        spinner.parentElement.removeChild(spinner);
    });
    xhr.onload = function() {
        let response = JSON.parse(xhr.responseText);
        if (xhr.status === 200) {
            document.getElementById('send-btn').removeAttribute('disabled');
            displayMessage('assistant', response.message);
        } else {
            displayMessage('error', response.error);
        }
    };
    xhr.send(JSON.stringify({message: message}));
    
    // Clear the input field
    messageInput.value = '';
}

function displayError(error) {
    let errorOuter = document.getElementById('error-msg');
    let errorInner = document.createElement('div');
    errorInner.classList.add('alert', 'alert-danger');
    errorInner.innerHTML = error;
    errorOuter.appendChild(errorInner);
}

function displayMessage(sender, message) {
    let chatContainer = document.getElementById('chat-container');
    let messageDiv = document.createElement('div');

    if (sender === 'error') {
        messageDiv.classList.add('error-message');
        
        // Create a span for the Chatbot text
        let chatbotSpan = document.createElement('span');
        chatbotSpan.innerHTML = "<b>Error:</b> ";
        messageDiv.appendChild(chatbotSpan);
        
        // Append the message to the Chatbot span
        messageDiv.innerHTML += message;
    } else if (sender === 'assistant') {
        messageDiv.classList.add('assistant-message');
        
        // Create a span for the Chatbot text
        let chatbotSpan = document.createElement('span');
        chatbotSpan.innerHTML = "<b>Chatbot:</b> ";
        messageDiv.appendChild(chatbotSpan);
        
        // Append the message to the Chatbot span
        messageDiv.innerHTML += message;
    } else {
        messageDiv.classList.add('user-message');

        let userSpan = document.createElement('span');
        userSpan.innerHTML = "<b>User:</b> ";
        messageDiv.appendChild(userSpan);
        
        // Append the message to the span
        messageDiv.innerHTML += message;
    }

    // Create a timestamp element
    let timestamp = document.createElement('span');
    timestamp.classList.add('timestamp');
    let currentTime = new Date().toLocaleTimeString();
    timestamp.innerText = " ["+ currentTime+"]";
    messageDiv.appendChild(timestamp);

    chatContainer.appendChild(messageDiv);

    // Scroll to the bottom of the chat container
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function clearError() {
    document.getElementById('error-msg').replaceChildren();
}

function clearChat() {
    document.getElementById('chat-container').replaceChildren();
}

// Handle button click event
let sendButton = document.getElementById('send-btn');
sendButton.addEventListener('click', sendMessage);

let input = document.getElementById("message-input");
input.addEventListener("keypress", function(e) {
  if (e.key === "Enter") {
    e.preventDefault();
    sendButton.click();
  }
});

let select = document.getElementById('function-select');
select.addEventListener('change', clearError);

let clearButton = document.getElementById('clear-btn');
clearButton.addEventListener('click', clearChat);
