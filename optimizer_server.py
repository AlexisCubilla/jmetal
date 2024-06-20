import logging
import websockets
import asyncio
import json
from calibration.optimizer import OptimizerWithCalibration
from observer import CustomObserver
from optimizer import Optimizer
import concurrent.futures
from dotenv import load_dotenv
import os
load_dotenv()
# url_pg="http://server/diagram"
# sim_url="ws://server/sim-optimizer"

connections = {}
optimizing = {}
observers = {}
async def handler(websocket):
    try:
        async for msg in websocket:
            await resolve(msg, websocket)
    except websockets.exceptions.ConnectionClosed:
        logging.info('Connection closed')


async def resolve(msg, websocket):
  
        parsed_message = json.loads(msg)
        print(parsed_message)
        await websocket.send(msg)
        action, scenario_id, project_id = parsed_message.get("action"), parsed_message.get("scenario_id"), parsed_message.get("project_id")
        
        if action == "optimize":
            if scenario_id in connections and scenario_id not in optimizing:
                    logging.info("Calculating solution for scenario %s", scenario_id)
                    optimizing[scenario_id] = True
                    observers[scenario_id] = CustomObserver()

                    op = OptimizerWithCalibration(connections[scenario_id])
                    progress=asyncio.create_task(send_optimization_progress(websocket, scenario_id))
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        optimizing[scenario_id], err = await asyncio.get_event_loop().run_in_executor(executor, op.optimize, scenario_id, project_id, observers[scenario_id])                    
                    if err:
                        optimizing.pop(scenario_id)
                        logging.error(err)
                    await progress

            if optimizing.get(scenario_id):
                    logging.info("Solution sent for scenario %s", scenario_id)
                    optimizing.pop(scenario_id)
                    # connections.pop(scenario_id)
                    # observers.pop(scenario_id)

        elif action == "init":
            if scenario_id not in connections: 
                connections[scenario_id] = websocket
            elif scenario_id in optimizing:
               await asyncio.create_task(send_optimization_progress(websocket, scenario_id))

        else:
            logging.warning("Unknown action: %s", action)

       

async def main():
    host = os.getenv("SIMULATION_WEBSOCKET_HOST")
    port = int(os.getenv("SIMULATION_WEBSOCKET_PORT"))
    async with websockets.serve(handler, host, port):
        print(f"Server started at ws://{host}:{port}")
        await asyncio.Future()


async def send_optimization_progress(websocket, scenario_id):
    ob:CustomObserver = observers[scenario_id]
    while websocket.open:
        if ob.solutions:
            data = {
                "action": "update",
                "progress": ob.porcetual_progress,
                "elapsed": ob.elapsed,
                "remaining": ob.remaining,
                "solutions": ob.solutions
            }
            await websocket.send(json.dumps(data))
            if ob.porcetual_progress >= 100:
                data["exiting"] = True
                await websocket.send(json.dumps(data))
                break
        await asyncio.sleep(0.1)

if __name__ == "__main__":
    asyncio.run(main())