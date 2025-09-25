import asyncio
import websockets
import json

# Store connected clients
clients = set()

async def handler(ws):
    print(" Client connected")
    clients.add(ws)
    try:
        async for message in ws:
            print(f" Received: {message}")

            try:
                data = json.loads(message)
            except json.JSONDecodeError:
                print(" Non-JSON message received, skipping...")
                continue

            # Broadcast message to all other clients
            for client in clients:
                if client != ws:
                    await client.send(json.dumps(data))

    except websockets.exceptions.ConnectionClosed:
        print(" Client disconnected")
    finally:
        clients.remove(ws)

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print(" WebSocket server running at ws://<PC_IP>:8765")
        await asyncio.Future()  # Keep server alive

if __name__ == "__main__":
    asyncio.run(main())
