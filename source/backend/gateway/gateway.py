import asyncio
from typing import ClassVar

import websockets

__all__: list[str] = ["Gateway"]


class Gateway:

    CONNECTIONS: ClassVar[list[websockets.WebsocketServerProtocol]] = []

    @classmethod
    async def deploy_gateway(
        cls, host: str | None = None, port: int | None = None
    ) -> None:
        async with websockets.serve(
            cls.register_connections, host, port, ping_interval=45, ping_timeout=20
        ) as websocket:
            await cls.event_manager(websocket)

    async def event_manager(
        self, websocket: websockets.WebsocketServerProtocol
    ) -> None:
        raise NotImplementedError()

    def authorizer(self, token: str) -> bool:
        username, password = token.split(":")
        # return True if the credentials are in the db, return False if not token must look like: username:password

    async def register_connections(
        self, websocket: websockets.WebsocketServerProtocol
    ) -> None:
        token = await websocket.recv()
        if self.authorizer(token):
            self.CONNECTIONS.append(websocket)
        else:
            await websocket.close(1011, "authentication failed")
        try:
            await websocket.wait_closed()
        finally:
            self.CONNECTIONS.remove(websocket)

    async def heart(self) -> None:
        while True:
            for connection in self.CONNECTIONS:
                try:
                    pong = await connection.ping("{eventcode: 0, data: {}}")
                    await pong
                except websockets.ConnectionClosed:
                    self.CONNECTIONS.remove(connection)
                finally:
                    await asyncio.sleep(45)

    async def send_message(self, text: str) -> None:
        asyncio.get_event_loop().run_in_executor(
            None, websockets.broadcast(self.CONNECTIONS, text)
        )
