frappe.after_ajax(function () {
    // Prevent adding multiple widgets
    if (document.getElementById("frappe-chatbot-widget")) return;

    // Create the wrapper div
    let chatbotWrapper = document.createElement("div");
    chatbotWrapper.id = "frappe-chatbot-widget";
    chatbotWrapper.innerHTML = `
        <div id="chatbot-toggle" style="
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: #4ae261ff;
            color: white;
            padding: 12px 18px;
            border-radius: 50%;
            cursor: pointer;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
            z-index: 9999;
            font-size: 20px;
        ">💬</div>

        <div id="chatbot-window" style="
            display: none;
            position: fixed;
            bottom: 80px;
            right: 20px;
            width: 350px;
            height: 450px;
            background: white;
            border-radius: 10px;
            box-shadow: 0px 4px 15px rgba(0,0,0,0.3);
            z-index: 9999;
            overflow: hidden;
            display: flex;
            flex-direction: column;
        ">
            <div style="background: #4A90E2; color: white; padding: 10px; font-weight: bold;">
                Frappe Assistant
                <span id="chatbot-close" style="float: right; cursor: pointer;">✖</span>
            </div>
            <div id="chatbot-messages" style="flex: 1; padding: 10px; overflow-y: auto; font-size: 14px;">
                <div style="color: gray; text-align: center;">Hello! How can I help you? 😊</div>
            </div>
            <div style="padding: 8px; display: flex; gap: 5px;">
                <input id="chatbot-input" type="text" placeholder="Type a message..." 
                       style="flex: 1; padding: 8px; border: 1px solid #ddd; border-radius: 5px;" />
                <button id="chatbot-send" style="
                    background: #4A90E2;
                    color: white;
                    border: none;
                    padding: 8px 12px;
                    border-radius: 5px;
                    cursor: pointer;
                ">Send</button>
            </div>
        </div>
    `;

    // Append to body so it appears everywhere
    document.body.appendChild(chatbotWrapper);

    // Get elements
    const toggleBtn = document.getElementById("chatbot-toggle");
    const chatWindow = document.getElementById("chatbot-window");
    const closeBtn = document.getElementById("chatbot-close");
    const sendBtn = document.getElementById("chatbot-send");
    const inputField = document.getElementById("chatbot-input");
    const messagesDiv = document.getElementById("chatbot-messages");

    // Toggle open
    toggleBtn.onclick = () => {
        chatWindow.style.display = "flex";
        inputField.focus();
    };

    // Close window
    closeBtn.onclick = () => {
        chatWindow.style.display = "none";
    };

    // Send message
    sendBtn.onclick = sendMessage;
    inputField.addEventListener("keypress", function (e) {
        if (e.key === "Enter") sendMessage();
    });

    function sendMessage() {
        let msg = inputField.value.trim();
        if (!msg) return;

        // Show user message
        let userMsg = document.createElement("div");
        userMsg.style.textAlign = "right";
        userMsg.innerHTML = `<span style="background:#e6f0ff; padding:5px 10px; border-radius:10px; display:inline-block; margin-bottom:5px;">${msg}</span>`;
        messagesDiv.appendChild(userMsg);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;

        inputField.value = "";

        // Simulated bot reply (replace with frappe.call for backend)
        setTimeout(() => {
            let botMsg = document.createElement("div");
            botMsg.innerHTML = `<span style="background:#f0f0f0; padding:5px 10px; border-radius:10px; display:inline-block; margin-bottom:5px;">You said: ${msg}</span>`;
            messagesDiv.appendChild(botMsg);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }, 500);
    }
});
