// Connect to websocket server
const ws_admin = new WebSocket("ws://localhost:8000/admin/ws");

// handle heartbeat
ws_admin.onmessage = function(event){
    const msg = JSON.parse(event.data);
    
    if (msg.eventcode == 0){
        ws_admin.send("1");
    }
}

function sendSettings(event){
    // Get toggle switch states
    const tog1s = document.getElementById("tog1").checked;
    const tog2s = document.getElementById("tog2").checked;
    const tog3s = document.getElementById("tog3").checked;
    const tog4s = document.getElementById("tog4").checked;
    const tog5s = document.getElementById("tog5").checked;
    
    // Create packet
    const msg = {
        type: "command",
        auth: "admin",
        features: {
            ai: tog1s,
            uep: tog2s,
            upep: tog3s,
            as: tog4s,
            de: tog5s
        },
        content: {}
    };
    
    // Send packet
    ws_admin.send(JSON.stringify(msg));
    
}

function backOut(event){
    ws_admin.close();
    window.location.href = "localhost:8000/";
}