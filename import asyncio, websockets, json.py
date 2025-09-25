import asyncio, websockets, json

async def handler(ws):
    while True:
        await asyncio.sleep(2)
        # Send fake data
        await ws.send(json.dumps({
            "type": "gesture",
            "gesture": "peace",
            "confidence": 95
        }))

async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print(" WebSocket server running at ws://localhost:8765")
        await asyncio.Future()  # keep running

asyncio.run(main())
