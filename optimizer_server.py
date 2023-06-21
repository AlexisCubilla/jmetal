import websockets
import asyncio
import json
from optimizer import Optimizer
import requests

url="http://sim.cybiraconsulting.local:3001"
action="get_scenario_model"
method="POST"
async def handler(websocket):
    while True:
        try:
            msg = await websocket.recv()
        except websockets.ConnectionClosedOK:
            break
        #send keep alive response
        await websocket.send(str(resolve(msg)))
        await websocket.close()    


def resolve(msg):
    parsed_message = json.loads(msg)
    action = parsed_message["action"]
    message = parsed_message["message"]
    if action == "optimize":
        project_id = message.get("project_id")
        scenario_id = message.get("scenario_id")
        scenario=request_model(project_id, scenario_id)
        op = Optimizer(scenario)
        solutions = op.optimize()
        return solutions
    return scenario


def request_model(project_id, scenario_id):
    data = {
    "method": method,
    "action": action,
    "project_id": project_id,
    "scenario_id":scenario_id
    }
    response = requests.post(url, json=data)

    if response.status_code == 200:
        result = response.text
    else:
        result = None
    return result




async def main():
    async with websockets.serve(handler, "optimizer.cybiraconsulting.local", 8001):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())