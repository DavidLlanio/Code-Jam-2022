import asyncio
import json
from typing import ClassVar

import websockets

from ..database import Admin, Credentials, Messages

__all__: list[str] = ["Gateway"]


class Gateway:
    """A class that represents the gateway for the chat room."""

    CONNECTIONS: ClassVar[list[dict[str, websockets.WebsocketServerProtocol]]] = []

    @classmethod
    async def deploy_gateway(
        cls, host: str | None = None, port: int | None = None
    ) -> None:
        """Method to initiate/deploy the gateway."""
        cls.messages = Messages.create_messages()
        cls.credentials = Credentials()
        cls.admin = Admin()

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
        elif websocket.path == "/register/ws":
            await self.register_account(websocket)

    async def register_account(
        self, websocket: websockets.WebsocketServerProtocol
    ) -> None:
        """Method to register an account to the database"""
        payload = await websocket.recv()
        await self.credentials.save_credentials(
            payload["username"], payload["password"], payload["image_url"]
        )
        await websocket.send("Welcome!")
        await websocket.close(1000, "Done!")

    async def admin_management(
        self, websocket: websockets.WebsocketServerProtocol
    ) -> None:
        """Method that manages admin connections"""
        current_settings = {}
        await websocket.send(current_settings)
        async for packet in websocket:
            payload = json.loads(packet)
            payload_eventcode = payload.get("eventcode")
            if payload_eventcode == 0:
                await websocket.ping("{eventcode: 0, data: {}}")
            elif payload_eventcode == 8:
                self.admin.add_permissions(
                    channel=payload["channel"],
                    randomize_username=payload["randomize_username"],
                    allow_edit_avatars=payload["allow_edit_avatars"],
                    allow_edit_messages=payload["allow_edit_messages"],
                    sort_by_alpha=payload["sort_by_alpha"],
                    double_english=payload["double_english"],
                )

    async def user_management(
        self, websocket: websockets.WebsocketServerProtocol
    ) -> None:
        """Method that manages regular user connections"""
        async for packet in websocket:
            payload = json.loads(packet)
            payload_eventcode = payload.get("eventcode")
            if payload_eventcode == 0:
                await websocket.ping("{eventcode: 0, data: {}}")
            elif payload_eventcode == 5:
                message_payload = {
                    "type": "message",
                    "user": payload.get("user", "Unknown User"),
                    "message": payload.get("message", "Hello World!"),
                }
                await self.send_message(message_payload)

    async def authorizer(self, token: str) -> bool:
        """Method to authorize certain users."""
        username, password = token.split(":")
        return await self.credentials.login(username, password)

    async def register_connections(
        self, websocket: websockets.WebsocketServerProtocol
    ) -> None:
        """Method for registering all new client connections."""
        payload = json.loads(await websocket.recv())
        if payload.get("eventcode") == 9:
            token = payload["data"]["token"]
        else:
            await websocket.close(1011, "Wrong Packet")
        if await self.authorizer(token):
            self.CONNECTIONS.append({token.split(":")[0]: websocket})
        else:
            await websocket.close(1011, "Authentication Failed")
        try:
            await websocket.wait_closed()
        finally:
            self.CONNECTIONS.remove(websocket)

    async def send_message(self, payload: dict[str, str]) -> None:
        """Method to send a message to all clients"""
        self.messages.add_message(payload["message"], payload["user"])
        (asyncio.get_event_loop() or asyncio.new_event_loop()).run_in_executor(
            None, websockets.broadcast(self.CONNECTIONS, payload["message"])
        )
