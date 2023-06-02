import websockets
import asyncio
import json
from optimizer import Optimizer

async def handler(websocket):
    while True:
        try:
            data = await websocket.recv()
        except websockets.ConnectionClosedOK:
            break
        #send keep alive response
        
        await websocket.send(str(resolve(data)))
        await websocket.close()    



def resolve(data):
    parsed_data = json.loads(data)
    action = parsed_data["action"]
    message = parsed_data["message"]
    has_int, has_float, has_binary = True, True, True
    if action == "optimize":
        if message.get("int") is None:
            has_int=False
        if message.get("float") is None:
            has_float=False
        if message.get("binary") is None:
            has_binary=False
        
    
        op = Optimizer(has_int, has_float, has_binary, message)
        solutions = op.optimize()
        return solutions
        
async def main():
    async with websockets.serve(handler, "localhost", 8001):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())