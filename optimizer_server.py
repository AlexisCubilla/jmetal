import websockets
import asyncio
import json
from database import Database
from optimizer import Optimizer
from websockets.sync.client import connect

# url_pg="http://server/diagram"
# sim_url="ws://server/sim-optimizer"
sim_url="ws://sim.cybiraconsulting.local:8001"
action="get_scenario_model"
method="POST"
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
        message = parsed_message["message"]
        scenario_id = message.get("scenario_id")
        project_id = message.get("project_id") 

        global solutions
        global connections
        
        if action == "optimize":
            if scenario_id not in connections:
                connections[scenario_id] = websocket
                with connect(sim_url, open_timeout=None, close_timeout=None) as sim_websocket:
                    message = {"action": "init","id": scenario_id,"project_id": project_id}
                    sim_websocket.send(str(json.dumps(message)))
                    receive_message(sim_websocket, "message")
                    db=Database()
                    scenario = db.get_scenario(project_id, scenario_id)
                    op = Optimizer()
                    solutions[scenario_id], err = op.optimize(scenario, sim_websocket)
                if err:
                    print(err)
            
            if solutions.get(scenario_id):
                print(solutions.get(scenario_id))
                await websocket.send(str(solutions[scenario_id]))
                print("Solution sent")

                
        elif action == "init":
            if scenario_id not in connections: #if the client is not already connected
                connections[scenario_id] = websocket
            elif solutions.get(scenario_id): #otherwise, if the solution for the client is already calculated
                await connections[scenario_id].send(solutions[scenario_id])
        
        else:
            print("Action not found")
        



def receive_message(websocket, condition):
    while True:
        message = websocket.recv()
        if condition in message:
            break
    return message


async def main():
    async with websockets.serve(handler, "optimizer.cybiraconsulting.local", 8001):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())