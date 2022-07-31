// Global variables
var currentEditUser;
var currentEditMsg;
var currentEditMsgID;
var currentEditImageURL;

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
document.getElementById("username").textContent = usern;

// Connect to websocket server
const ws_chat = new WebSocket("ws://localhost:8000/chatroom.html/ws");

ws_chat.onmessage = function (event) {
    const msg = JSON.parse(event.data);

    switch (msg.eventcode) {
        // Handle Heartbeat
        case 0:
            console.log("pong")
            ws_chat.send('1');
            break;
        // Handle username/img change
        case 3:
            break;
        // Handle message
        case 5:
            if (msg.user === usern) {
                creatUserMessage(msg.user, msg.message,
                    msg.messageID, msg.time);
            }
            else {
                creatNonUserMessage(msg.user, msg.message,
                    msg.messageID, msg.time);
            }
            break;
        // Handle message change
        case 6:
            break;

    }
}

function sendMessage(event) {
    const umsg = document.getElementById("userInput").value;
    const msg = {
        eventcode: 5,
        user: usern,
        message: umsg
    };

    // Send packet
    ws_chat.send(JSON.stringify(msg));
}

function creatNonUserMessage(user, mesg, mesgID, time) {
    const root = document.getElementById("messagelist");
    root.innerHTML += ' \
      <li id="{_mesgID}" class="list-group-item"> \
      <div class="container" style="border-style: solid;"> \
      <img class="rounded-circle" src="https://cataas.com/cat/says/hello%20world!" width="50" height="50" style="margin: 0px;margin-top: 5px;margin-right: 5px;margin-bottom: 5px;" /> \
      <span id="messageUser">{_user}</span> \
      <p id="messageContent>{_mesg}</p> \
      <span>{_time}</span> \
      <button class="btn btn-primary float-end" type="button" style="font-size: 10px;padding-bottom: 0px;padding-top: 2px;">Edit</button> \
      </div> \
      </li> \
    '.formatUnicorn({
        _mesgID: mesgID, _user: user, _mesg: mesg, _time: time
    });
}

function creatUserMessage(user, mesg, mesgID, time) {
    const root = document.getElementById("messagelist");
    root.innerHTML += ' \
      <li id="{_mesgID}" class="list-group-item"> \
      <div class="container" style="border-style: solid;"> \
      <img class="rounded-circle" src="https://cataas.com/cat/says/hello%20world!" width="50" height="50" style="margin: 0px;margin-top: 5px;margin-right: 5px;margin-bottom: 5px;" /> \
      <span id="messageUser">{_user}</span> \
      <p id="messageContent">{_mesg}</p> \
      <span>{_time}</span> \
      </div> \
      </li> \
    '.formatUnicorn({
        _mesgID: mesgID, _user: user, _mesg: mesg, _time: time
    });
}

function editUser(event, elem) {
    const regex1 = /(?<="messageUser">)[\w\s]+/g;
    currentEditUser = String(elem.parentElement.innerHTML.match(regex1));

    currentEditMsg = elem.previousSibling.previousSibling.textContent;

    currentEditImageURL = elem.previousElementSibling.previousElementSibling.previousElementSibling.previousElementSibling.src;

    currentEditMsgID = elem.parentElement.parentElement.id;

    editPopup();


}

function editPopup() {
    const elem = document.getElementById("popupform");
    elem.style.display = "block";

    var formChildren = elem.firstElementChild.children;

    // Placeholder username
    formChildren[2].placeholder = currentEditUser;

    // Placeholder message
    formChildren[3].placeholder = currentEditMsg;

    // Placeholder imageURL
    formChildren[4].placeholder = currentEditImageURL;
}

function editSendButton(event) {
    const elem = document.getElementById("popupform");

    var formChildren = elem.firstElementChild.children;

    // Get user if changed
    var userVal = formChildren[2].value;
    if (userVal === "") {
        userVal = currentEditUser;
    }

    // Get message if changed
    var msgVal = formChildren[3].value;
    if (msgVal === "") {
        msgVal = currentEditMsg;
    }

    // Get ImageURL if changed
    var imageVal = formChildren[4].value;
    if (imageVal === "") {
        imageVal = currentEditImageURL;
    }

    // Send changes to server
    const commUser = {
        eventcode: 3,
        auth: "user",
        features: {},
        content: {
            user: { currentEditUser: userVal },
            img: { currentEditImagURL: imageVal },
        }
    };

    const commMesg = {
        eventcode: 6,
        auth: "user",
        features: {},
        content: {
            msg: { currentEditMsg: msgVal },
            msgID: currentEditMsgID
        }
    };

    // Send packet
    ws_chat.send(JSON.stringify(commUser));
    ws_chat.send(JSON.stringify(commMesg));

    updateMessage(currentEditMsgID, msgVal);

    elem.style.display = "none";
}

function updateUser(oldU, newU, oldIm, newIm) {
    // If nothing changed, return
    if (oldU == newU && oldIm == newIm) {
        return;
    }

    const msglist = document.getElementById("messagelist");

    var messages = msglist.children;

    for (var i = 0; i < messages.length; i++) {
        var content = messages[i].firstElementChild.children;
        var username = content[1].textContent;
        if (username == oldU) {
            content[1].textContent = newU;
            content[0].src = newIm;
        }
    }
}

function updateMessage(msgID, newMsg) {
    const msglist = document.getElementById("messagelist");

    var messages = msglist.children;

    for (var i = 0; i < messages.length; i++) {
        if (messages[i].id == msgID) {
            var content = messages[i].firstElementChild.children;
            content[2].innerHTML = newMsg;
        }
    }
}

function editCancelButton() {
    document.getElementById("popupform").style.display = "none";
}

function leaveButton(event) {
    ws_chat.close();
    window.location.href = "/";
}
