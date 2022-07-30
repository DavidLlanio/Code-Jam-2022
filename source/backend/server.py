from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from .admin_utils import Settings

settings = Settings()
app = FastAPI()

# chat_client_list = []


# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     """Websocket endpoint for communications in a chat room"""
#     await websocket.accept()
#     if websocket not in chat_client_list:
#         chat_client_list.append(websocket)
#     while True:
#         data = await websocket.receive_text()
#         for client in chat_client_list:
#             if websocket != client:
#                 await client.send_text(f"{data}")


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
                            "features": settings.return_frontend_settings(),
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

            # maps the settings from the received frontend shorthand names to the longform backend names
            received_settings = data.get("features", None)
            settings_remap = {
                "ai": "randomize_username",
                "allow_edit_messages": "uep",
                "allow_edit_avatars": "upep",
                "sort_by_alpha": "as",
                "double_english": "de",
            }
            mapped_settings = {
                settings_remap[k]: received_settings[k] for k in received_settings
            }

            if mapped_settings:
                settings.update_settings(mapped_settings)

            # TODO: notify chat clients when settings have changed
            # figure out changed setting
            # act based on setting changes
            #   make db changes to chat messages/users if needed
            #   notify chat clients, if needed

            # sends an updated list of settings to all admin clients
            # TODO: update to only send settings that have been updated
            for admin_client in admin_client_list:
                if admin_client != websocket:
                    await websocket.send_json(
                        {"features": settings.return_frontend_settings()}
                    )

    except WebSocketDisconnect:
        if websocket in admin_client_list:
            admin_client_list.remove(websocket)
