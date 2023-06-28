import websockets
import asyncio
import json
from database import Database
from optimizer import Optimizer

# url_pg="http://server/diagram"
# sim_url="ws://server/sim-optimizer"

connections = {}
solutions = {}

async def handler(websocket):
    while True:
        try:
            msg = await websocket.recv()
        except websockets.ConnectionClosed as exc:
            if exc.code == 1006 or exc.code == 1005 or exc.code == 1000:
                print('Connection closed')
                break
        asyncio.create_task(resolve(msg, websocket))


async def resolve(msg, websocket):
        parsed_message = json.loads(msg)
        action = parsed_message["action"]
        scenario_id = parsed_message.get("scenario_id")
        project_id = parsed_message.get("project_id") 

        global solutions
        global connections
        if action == "optimize":
            if scenario_id not in solutions and scenario_id in connections: #if the solution for the client is not calculated yet but the client is already connected
                connections[scenario_id] = websocket
                op = Optimizer()
                solutions[scenario_id], err = op.optimize(scenario_id, project_id)
                if err:
                    print(err)
            if solutions.get(scenario_id):
                await websocket.send(json.dumps({"exiting":True, "message":solutions[scenario_id]}))
                print("Solution sent")
                solutions.pop(scenario_id)
                connections.pop(scenario_id)
                
        elif action == "init":
            if scenario_id not in connections: #if the client is not already connected
                connections[scenario_id] = websocket
            # elif solutions.get(scenario_id): #otherwise, if the solution for the client is already calculated
            #     await connections[scenario_id].send(solutions[scenario_id])
        
        else:
            print("Action not found")
        

async def main():
    async with websockets.serve(handler, "optimizer.cybiraconsulting.local", 8001):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())