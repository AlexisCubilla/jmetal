import asyncio
import json
import random
import websockets
utility = 10000
async def handler(websocket):
    while True:
        try:
            message = await websocket.recv()
        except websockets.ConnectionClosedOK:
            break
        await websocket.send(resolve(message))

def resolve(message):
    global utility
    data = json.loads(message)
    print(data)
    # {'id': 'uuid', 'period': 1, 'type': 'calibration', 'utility': 'utility', 'outputs': [{'id': 'uuid', 'value': 0}, {'id': 'uuid', 'value': 1}], 'inputs': [{'id': 'uuid', 'value': 0}, {'id': 'uuid', 'value': 0}]}
    
    
    utilities = [utility]
    utility -= 1
    constraints = [random.choice([-1, 1]) for _ in range(2)]
    reply = {
        "utilities": utilities,
        "constraints": constraints
    }
    return json.dumps(reply)


async def main():
    async with websockets.serve(handler, "localhost", 8008):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())