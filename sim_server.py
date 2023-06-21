import asyncio
import random
import websockets

async def handler(websocket):
    while True:
        try:
            message = await websocket.recv()
        except websockets.ConnectionClosedOK:
            break
        await websocket.send(resolve(message))

def resolve(message):
    parsed_message = eval(message)
    # first_sum = int(parsed_message["int"][0]) + int(parsed_message["int"][1])
    # second_sum = float(parsed_message["float"][0]) + float(parsed_message["float"][1])
    reply=str([random.randint(0, 100), random.randint(0, 100)])
    return reply

async def main():
    async with websockets.serve(handler, "localhost", 8000):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())