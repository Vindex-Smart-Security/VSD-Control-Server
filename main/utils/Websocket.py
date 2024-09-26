import asyncio
import websockets
import json
import socket
from utils.Setup import log_message
import time

async def handle_client(websocket, path):
    """Handle incoming WebSocket connections."""

    device_info = {
        "hostname": socket.gethostname(),
        "ip_address": socket.gethostbyname(socket.gethostname()),
    }

    token = "aB3cD4eF5gH6iJ7kL8mN9oPqR"

    message = {
        "data": device_info,
        "auth": token
    }

    await websocket.send(json.dumps(message))

    async for message in websocket:
        await websocket.send(f"Echo: {message}")

async def start_server():
    """Start the WebSocket server."""
    time.sleep(3)
    log_message("WebSocket Successfully Connected", level="SUCCESS")
    time.sleep(3)
    log_message("WebSocket Running ws:localhost:6789", level="INFO")
    server = await websockets.serve(handle_client, "localhost", 6789)
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(start_server())
