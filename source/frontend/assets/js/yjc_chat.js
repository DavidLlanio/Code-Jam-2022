// Funciton to format strings
String.prototype.formatUnicorn = String.prototype.formatUnicorn ||
function () {
    "use strict";
    var str = this.toString();
    if (arguments.length) {
        var t = typeof arguments[0];
        var key;
        var args = ("string" === t || "number" === t) ?
            Array.prototype.slice.call(arguments)
            : arguments[0];

        for (key in args) {
            str = str.replace(new RegExp("\\{" + key + "\\}", "gi"), args[key]);
        }
    }

    return str;
};

// Get the username input by user and set as username
var usern = sessionStorage.getItem("usern");
document.getElementById("username").textContent=usern;

// Connect to websocket server
const ws_chat = new WebSocket("ws://localhost:8000/chat/ws");

ws_chat.onmessage = function(event){
    const msg = JSON.parse(event.data);
    
    switch(msg.eventcode){
        // Handle Heartbeat
        case 0:
           ws_admin.send("1");
           break;
        // Handle message
        case 1:
           if (msg.user === usern){
               creatUserMessage(msg.user, msg.message, 
                                msg.messageID, msg.time);
           }
           else{
               creatNonUserMessage(msg.user, msg.message, 
                                msg.messageID, msg.time);
           }
            
    }
}

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

function creatNonUserMessage(user, mesg, mesgID, time){
    const root = document.getElementById("messagelist");
    root.innerHTML += ' \
      <li id="{_mesgID}" class="list-group-item"> \
      <div class="container" style="border-style: solid;"> \
      <img class="rounded-circle" src="https://cataas.com/cat/says/hello%20world!" width="50" height="50" style="margin: 0px;margin-top: 5px;margin-right: 5px;margin-bottom: 5px;" /> \
      <span>{_user}</span> \
      <p>{_mesg}</p> \
      <span>{_time}</span> \
      <button class="btn btn-primary float-end" type="button" style="font-size: 10px;padding-bottom: 0px;padding-top: 2px;">Edit</button> \
      </div> \
      </li> \
    '.formatUnicorn({
        _mesgID:mesgID, _user:user, _mesg:mesg, _time:time
    });
}

function creatUserMessage(user, mesg, mesgID, time){
    const root = document.getElementById("messagelist");
    root.innerHTML += ' \
      <li id="{_mesgID}" class="list-group-item"> \
      <div class="container" style="border-style: solid;"> \
      <img class="rounded-circle" src="https://cataas.com/cat/says/hello%20world!" width="50" height="50" style="margin: 0px;margin-top: 5px;margin-right: 5px;margin-bottom: 5px;" /> \
      <span>{_user}</span> \
      <p>{_mesg}</p> \
      <span>{_time}</span> \
      </div> \
      </li> \
    '.formatUnicorn({
        _mesgID:mesgID, _user:user, _mesg:mesg, _time:time
    });   
}

function leaveButton(event){
    ws_chat.close();
    window.location.href = "localhost:8000/";
}