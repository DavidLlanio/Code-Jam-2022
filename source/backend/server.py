from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from .admin_utils import Settings

app = FastAPI()

chat_client_list = []
settings = Settings()


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
    try:
        while True:
            # admin must enter password before they can change settings
            # this is tracked server-side per websocket
            while input_password != admin_password:
                data = await websocket.receive_json()
                input_password = data.get("password", None)
                if input_password == admin_password:
                    await websocket.send_json(
                        {
                            "message": "correct password",
                            "settings": settings.get_settings(),
                        }
                    )
                    admin_client_list.append(websocket)
                    break
                elif input_password is None:
                    await websocket.send_json({"message": "missing password"})
                else:
                    await websocket.send_json({"message": "incorrect password"})

            # monitors websocket for changes to the settings
            data = await websocket.receive_json()
            if updated_settings := data.get("settings", None):
                settings.update_settings(updated_settings)

            # TODO: notify chat clients when settings have changed
            # figure out changed setting
            # act based on setting changes
            #   make db changes to chat messages/users if needed
            #   notify chat clients, if needed

            # sends an update list to all admin clients
            # TODO: update to only send settings that have been updated
            for admin_client in admin_client_list:
                if admin_client != websocket:
                    await websocket.send_json({"settings": settings.get_settings()})

    except WebSocketDisconnect:
        if websocket in admin_client_list:
            admin_client_list.remove(websocket)
