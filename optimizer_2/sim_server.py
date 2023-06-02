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
    print(message)
    parsed_message = eval(message)
    first_sum = int(parsed_message["int"][0]) + int(parsed_message["int"][1])
    second_sum = int(parsed_message["float"][0]) + int(parsed_message["float"][1])
    reply=str([first_sum,second_sum, parsed_message["binary"]])
    print(reply)
    return reply

async def main():
    async with websockets.serve(handler, "localhost", 8000):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())