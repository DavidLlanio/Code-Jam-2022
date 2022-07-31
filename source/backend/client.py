from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn

client = FastAPI()
client.mount("/", StaticFiles(directory="../frontend", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(client, host="127.0.0.1", port=8001)  # TODO change this to int(os.getenv('APP_PORT'))
