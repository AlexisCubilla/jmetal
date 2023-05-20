import asyncio
import websockets

async def handler(websocket):
    while True:
        try:
            message = await websocket.recv()
        except websockets.ConnectionClosedOK:
            break
        await websocket.send(resolve(message))

def resolve(message):
    reply = f"{[sum(eval(message))]}"
    return reply

async def main():
    async with websockets.serve(handler, "localhost", 8000):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())