frappe.after_ajax(function () {
    if (document.getElementById("frappe-chatbot-widget")) return;

    // Create wrapper
    let chatbotWrapper = document.createElement("div");
    chatbotWrapper.id = "frappe-chatbot-widget";
    chatbotWrapper.innerHTML = `
        <!-- Tooltip / Initial Message -->
        <div id="chatbot-tooltip" style="
            display: block; /* show by default */
            position: fixed;
            bottom: 85px;
            right: 20px;
            background: #4A90E2;
            color: white;
            padding: 10px 14px;
            border-radius: 10px;
            font-size: 14px;
            font-weight: 500;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.2);
            z-index: 9999;
            white-space: nowrap;
        ">
            👋 How may I assist you?
        </div>

        <!-- Toggle Button -->
        <div id="chatbot-toggle" style="
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: #4A90E2;
            color: white;
            width: 55px;
            height: 55px;
            border-radius: 50%;
            cursor: pointer;
            box-shadow: 0px 4px 15px rgba(0,0,0,0.2);
            z-index: 9999;
            font-size: 26px;
            display: flex;
            align-items: center;
            justify-content: center;
        ">💬</div>

        <!-- Chat Window -->
        <div id="chatbot-window" style="
            display: none;
            position: fixed;
            bottom: 85px;
            right: 20px;
            width: 360px;
            height: 480px;
            background: white;
            border-radius: 12px;
            box-shadow: 0px 8px 25px rgba(0,0,0,0.25);
            z-index: 9999;
            overflow: hidden;
            flex-direction: column;
            font-family: system-ui, sans-serif;
        ">
            <div style="background: #4A90E2; color: white; padding: 12px; font-weight: 600; display: flex; justify-content: space-between; align-items: center;">
                Scholarship Assistant
                <span id="chatbot-close" style="cursor: pointer; font-size: 18px;">✖</span>
            </div>
            <div id="chatbot-messages" style="flex: 1; padding: 12px; overflow-y: auto; background: #f9f9f9; font-size: 14px;">
                <div style="color: gray; text-align: center; font-style: italic; margin-bottom: 10px;">
                    👋 Hello! How can I help you today?
                </div>
            </div>
            <div style="padding: 10px; background: #fff; border-top: 1px solid #ddd; display: flex; gap: 8px;">
                <input id="chatbot-input" type="text" placeholder="Type your message..." style="flex: 1; padding: 8px 10px; border: 1px solid #ccc; border-radius: 20px; outline: none;" />
                <button id="chatbot-send" style="background: #4A90E2; color: white; border: none; padding: 8px 14px; border-radius: 20px; cursor: pointer; font-weight: bold;">➤</button>
            </div>
        </div>
    `;
    document.body.appendChild(chatbotWrapper);

    // Elements
    const toggleBtn = document.getElementById("chatbot-toggle");
    const tooltip = document.getElementById("chatbot-tooltip");
    const chatWindow = document.getElementById("chatbot-window");
    const closeBtn = document.getElementById("chatbot-close");
    const sendBtn = document.getElementById("chatbot-send");
    const inputField = document.getElementById("chatbot-input");
    const messagesDiv = document.getElementById("chatbot-messages");

    // Show chat window on toggle click and hide tooltip
    toggleBtn.onclick = () => {
        tooltip.style.display = "none"; // hide the initial message
        chatWindow.style.display = "flex";
        inputField.focus();
    };

    // Close chat window
    closeBtn.onclick = () => {
        chatWindow.style.display = "none";
    };

    // Send events
    sendBtn.onclick = sendMessage;
    inputField.addEventListener("keypress", (e) => {
        if (e.key === "Enter") sendMessage();
    });

    // Add message to chat
    function addMessage(content, type) {
        let msgDiv = document.createElement("div");
        msgDiv.style.marginBottom = "8px";

        if (type === "user") {
            msgDiv.style.textAlign = "right";
            msgDiv.innerHTML = `<span style="background: #e6f0ff; padding: 6px 10px; border-radius: 15px; display: inline-block; max-width: 80%; word-wrap: break-word;">${content}</span>`;
        } else {
            msgDiv.innerHTML = `<span style="background: #f0f0f0; padding: 6px 10px; border-radius: 15px; display: inline-block; max-width: 80%; word-wrap: break-word;">${content}</span>`;
        }

        messagesDiv.appendChild(msgDiv);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }

    // Send message to server
    function sendMessage() {
        let msg = inputField.value.trim();
        if (!msg) return;

        addMessage(msg, "user");
        inputField.value = "";

        frappe.call({
            method: "scholarship_management.api.chatbot_reply",
            args: { message: msg },
            callback: function (r) {
                if (Array.isArray(r.message)) {
                    r.message.forEach((line, index) => {
                        setTimeout(() => addMessage(line, "bot"), index * 500);
                    });
                } else if (r.message) {
                    addMessage(r.message, "bot");
                } else {
                    addMessage("Sorry, I didn’t understand that.", "bot");
                }
            }
        });
    }
});
