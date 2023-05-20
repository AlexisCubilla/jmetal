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
        print(data)
        await websocket.send(str(resolve(data)))


def resolve(data):
    parsed_data = json.loads(data)
    action = parsed_data["action"]
    message = parsed_data["message"]

    if action == "optimize":
        lower_bound_list = message["variable"]["lower_bound_list"]
        upper_bound_list = message["variable"]["upper_bound_list"]
        max_evaluations = message["max_evaluations"]
        op=Optimizer()
        solutions=op.optimize(lower_bound_list, upper_bound_list, max_evaluations, 1)
        return op.process_results(solutions)

       
async def main():
    async with websockets.serve(handler, "localhost", 8001):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())