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
    parsed_message = eval(message)
    first_sum = parsed_message[0]+ parsed_message[1]
    second_sum = parsed_message[2] + parsed_message[3]
    reply=str([first_sum,second_sum])
    return reply

async def main():
    async with websockets.serve(handler, "localhost", 8000):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())