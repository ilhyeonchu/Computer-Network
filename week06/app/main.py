import socket

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": f"Hello from {socket.gethostname()}"}
