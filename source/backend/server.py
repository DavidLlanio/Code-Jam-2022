from fastapi import FastAPI, WebSocket
import uvicorn
import asyncio

# creating FastAPI application
app = FastAPI()


@app.websocket("/chatroom.html/ws")
async def websocket_chat_endpoint(websocket: WebSocket):
    print('Accepting client connection...')
    await websocket.accept()
    while True:
        try:
            await heartbeat(websocket)
        except Exception as e:
            print('error:', e)
            break
    print('Terminating connection...')


@app.websocket("/adminpanel.html/ws")
async def websocket_admin_endpoint(websocket: WebSocket):
    print('Accepting client-admin connection...')
    await websocket.accept()
    while True:
        try:
            print('hi')
        except Exception as e:
            print('error:', e)
            break
    print('Terminating connection...')


async def heartbeat(websocket):
    """
    Send and process heartbeat ping from client
    """
    # Sending heartbeat to client
    msg = {"eventcode": 0}
    await websocket.send_json(msg)
    print("ping")

    # Receiving heartbeat from client
    rcvd_msg = await websocket.receive_text()
    if str(rcvd_msg) == "1":
        print("heartbeat received")
    else:
        print("invalid response")
    # Heartbeat sent every 45 seconds
    await asyncio.sleep(2)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)  # TODO change this to int(os.getenv('APP_PORT'))
