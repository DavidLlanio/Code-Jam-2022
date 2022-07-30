from fastapi import FastAPI, WebSocket
import asyncio

# creating FastAPI application
app = FastAPI()
test = 0


@app.websocket("/chat/ws")
async def websocket_endpoint(websocket: WebSocket):
    print('Accepting client connection...')
    await websocket.accept()
    while True:
        try:
            await heartbeat(websocket)
        except Exception as e:
            print('error:', e)
            break
    print('Bye..')


async def heartbeat(websocket):
    """
    Send and process heartbeat ping from client
    """
    # Sending heartbeat to client
    msg = {"eventcode": 0}
    await websocket.send_json(msg)

    # Receiving heartbeat from client
    rcvd_msg = await websocket.receive_text()
    if str(rcvd_msg) == "1":
        print("heartbeat received")
    else:
        print("invalid response")
    # Heartbeat sent every 45 seconds
    await asyncio.sleep(45)
