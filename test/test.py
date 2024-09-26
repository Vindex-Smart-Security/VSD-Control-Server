import asyncio
import websockets
import json
import random
import string

# Function to generate a random token
def generate_token(length=16):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# Function to create a WebSocket connection and send data
async def send_auth_message(uri):
    token = generate_token()  # Generate a random token
    device_info = {
        "DATA": {
            "Auth": token,
            "Device": "TestDevice",
            "Version": "1.0"
        }
    }
    
    async with websockets.connect(uri) as websocket:
        # Send the authentication message
        await websocket.send(json.dumps(device_info))
        print(f"Sent: {device_info}")

        # Optionally wait for a response
        response = await websocket.recv()
        print(f"Received: {response}")

if __name__ == "__main__":
    server_uri = "ws://localhost:6789"  # Replace with your server's WebSocket URI
    asyncio.run(send_auth_message(server_uri))
