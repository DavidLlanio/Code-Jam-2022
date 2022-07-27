function chatPress(){
    const username = document.getElementById("username");
    const pass = document.getElementById("imageurl");
    
    if (pass === "www.admin123.com"){
        window.location.href = "localhost:8000/admin";
    } else {
        sessionStorage.setItem("usern", username);
        window.location.href = "localhost:8000/chat";
    }
}