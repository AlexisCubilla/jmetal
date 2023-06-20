import websockets
import asyncio
import json
from optimizer import Optimizer
import requests
from data import Data

url="http://localhost:3001"
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
        data = get_data(scenario)
        op = Optimizer(data)
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
        result = json.loads(response.text)
    else:
        result = None
    return result

def get_data(scenario):
    data = Data()

    variables = scenario["optimization"][0]["optimization_variables"]
    functions = scenario["optimization"][0]["optimization_functions"]

    for var in variables:
        businessObject = var["businessObject"]
        print(businessObject)
        if businessObject["type"] == "I":
            data.int_lower_bound.append(businessObject["lower_bound"])
            data.int_upper_bound.append(businessObject["upper_bound"])
        elif businessObject["type"] == "F":
            data.float_lower_bound.append(businessObject["lower_bound"])
            data.float_upper_bound.append(businessObject["upper_bound"])
        elif businessObject["type"] == "B":
            data.number_of_bits += 1

    data.has_int = bool(data.int_lower_bound)
    data.has_float = bool(data.float_lower_bound)
    data.has_binary = bool(data.number_of_bits)

    for fn in functions:
        data.directions.append(fn["direction"])

    businessObject = scenario["optimization"][0]["businessObject"]
    data.number_of_objectives = len(functions)
    data.max_evaluations = businessObject["stop_criteria"]["max_evaluations"]
    data.population = businessObject["population"]
    data.offspring_population = businessObject["offspring_population"]
    # data.simulation_periods = businessObject["simulation_periods"]

    return data

async def main():
    async with websockets.serve(handler, "localhost", 8001):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())