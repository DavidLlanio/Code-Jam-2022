import asyncio
import json
import os
from typing import ClassVar

import database
import websockets

from ..admin_utils import Settings

__all__: list[str] = ["Gateway"]
settings = Settings()
admin_password = os.getenv("USERNAME", "secret")


class Gateway:
    """A class that represents the gateway for the chat room."""

    CONNECTIONS: ClassVar[list[dict[str, websockets.WebsocketServerProtocol]]] = []

    @classmethod
    async def deploy_gateway(
        cls, host: str | None = None, port: int | None = None
    ) -> None:
        """Method to initiate/deploy the gateway."""
        async with websockets.serve(
            cls.register_connections, host, port, ping_interval=45, ping_timeout=20
        ) as websocket:
            await cls.connections_manager(websocket)

    async def connections_manager(
        self, websocket: websockets.WebsocketServerProtocol
    ) -> None:
        """Method that handles all incoming websocket connections."""
        if websocket.path == "/admin/ws":
            await self.admin_management(websocket)
        elif websocket.path == "/chat/ws":
            await self.user_management(websocket)

    async def admin_management(self, websocket: websockets.WebsocketServerProtocol):
        """Method that manages admin connections"""
        current_settings = {}
        await websocket.send(current_settings)
        async for packet in websocket:
            payload = json.loads(packet)
            match payload.get("eventcode"):
                case 0:
                    await websocket.ping("{eventcode: 0, data: {}}")
                case 8:
                    # TODO: figure out how to do admin password checking in gateway
                    # while input_password != admin_password:
                    #     data = await websocket.receive_json()
                    #     input_password = data.get("password", None)
                    #     if input_password == admin_password:
                    #         await websocket.send_json(
                    #             {
                    #                 "message": "correct password",
                    #                 "features": settings.return_frontend_settings(),
                    #             }
                    #         )
                    #         # admin_client_list.append(websocket)
                    #         break
                    #     elif input_password is None:
                    #         await websocket.send_json({"message": "missing password"})
                    #     else:
                    #         await websocket.send_json({"message": "incorrect password"})

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
                        settings_remap[k]: received_settings[k]
                        for k in received_settings
                    }

                    if mapped_settings:
                        settings.update_settings(mapped_settings)

                    # TODO: notify chat clients when settings have changed

                    # sends an updated list of settings to all admin clients
                    # TODO: send out to all admin websocket connections
                    # for admin_client in admin_client_list:
                    #     if admin_client != websocket:
                    #         await websocket.send_json(
                    #             {"features": settings.return_frontend_settings()}
                    #         )

                case other:
                    pass

    async def user_management(self, websocket: websockets.WebsocketServerProtocol):
        """Method that manages regular user connections"""
        async for packet in websocket:
            payload = json.loads(packet)
            messages = database.Messages()
            match payload.get("eventcode"):
                case 0:
                    await websocket.ping("{eventcode: 0, data: {}}")
                case 5:
                    # save the payload to the db
                    message_id = messages.add_message(
                        current_text="Hello world", sender_username="Unknown User"
                    )
                    message_payload = {
                        "type": "message",
                        "user": payload.get("user", "Unknown User"),
                        "message": payload.get("message", "Hello World!"),
                        "uid": message_id,
                    }

                    await self.send_message(message_payload)

    def authorizer(self, token: str) -> bool:
        """Method to authorize certain users."""
        username, password = token.split(":")
        # return True if the credentials are in the db, return False if not token must look like: username:password

    async def register_connections(
        self, websocket: websockets.WebsocketServerProtocol
    ) -> None:
        """Method for registering all new client connections."""
        token = await websocket.recv()
        if self.authorizer(token):
            self.CONNECTIONS.append({token.split(":")[0]: websocket})
        else:
            await websocket.close(1011, "authentication failed")
        try:
            await websocket.wait_closed()
        finally:
            self.CONNECTIONS.remove(websocket)

    async def send_message(self, payload: dict[str, str]) -> None:
        """Method to send a message to all clients"""
        (asyncio.get_event_loop() or asyncio.new_event_loop()).run_in_executor(
            None, websockets.broadcast(self.CONNECTIONS, payload["message"])
        )
