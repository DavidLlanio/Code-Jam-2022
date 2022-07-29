// Get the username input by user and set as username
var usern = sessionStorage.getItem("usern");
document.getElementById("username").textContent=usern;

// Connect to websocket server
const ws_chat = new WebSocket("ws://localhost:8000/admin/ws");

function sendMessage(event){
    const umsg = document.getElementById("userInput").value;
    const msg = {
        type: "message"
        user: usern,
        message: umsg
    };
    
    // Send packet
    ws_chat.send(JSON.stringify(msg));
}

function leaveButton(event){
    ws_chat.close();
    window.location.href = "localhost:8000/";
}