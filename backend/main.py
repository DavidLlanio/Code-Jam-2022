from fastapi import FastAPI, WebSocket

app = FastAPI()

chat_client_list = []


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Websocket endpoint for communications in a chat room"""
    await websocket.accept()
    if websocket not in chat_client_list:
        chat_client_list.append(websocket)
    while True:
        data = await websocket.receive_text()
        for client in chat_client_list:
            if websocket != client:
                await client.send_text(f"{data}")


admin_password = "secret"
admin_client_list = []


# TODO: initialization, persistance, affect data
@app.websocket("/ws/admin")
async def admin_websocket(websocket: WebSocket):
    """Websocket endpoint for handling admin updates"""
    await websocket.accept()
    input_password = ""
    while True:
        while input_password != admin_password:
            data = await websocket.receive_json()
            input_password = data.get("password", None)
            if input_password == admin_password:
                await websocket.send_json({"message": "correct password"})
                break
            await websocket.send_json({"message": "incorrect or missing password"})

        data = await websocket.receive_json()
        print(data)