function chatPress(){
    const username = document.getElementById("username");
    const pass = document.getElementById("imageurl");
    
    if (pass === "www.admin123.com"){
        window.location.href = "localhost:8001/adminpanel.html";
    } else {
        sessionStorage.setItem("usern", username);
        window.location.href = "http://localhost:8001/chatroom.html";
    }
}