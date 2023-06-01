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

    if action == "optimize":
        int_lower_bound = message["int"]["lower_bound"]
        int_upper_bound = message["int"]["upper_bound"]
        float_lower_bound = message["float"]["lower_bound"]
        float_upper_bound = message["float"]["upper_bound"]
        number_of_bits = message["binary"]["number_of_bits"]
        max_evaluations = message["max_evaluations"]
        number_of_objectives_count = message["number_of_objectives"]
        op = Optimizer()
        solutions = op.optimize(int_lower_bound, int_upper_bound, float_lower_bound, float_upper_bound, number_of_bits, max_evaluations, number_of_objectives_count)
        return solutions
        
async def main():
    async with websockets.serve(handler, "localhost", 8001):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())