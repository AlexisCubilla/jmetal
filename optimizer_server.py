import logging
import websockets
import asyncio
import json
from observer import CustomObserver
from optimizer import Optimizer
import concurrent.futures

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
        action, scenario_id, project_id = parsed_message.get("action"), parsed_message.get("scenario_id"), parsed_message.get("project_id")

        if action == "optimize":
            if scenario_id in connections and scenario_id not in optimizing:
                    logging.info("Calculating solution for scenario %s", scenario_id)
                    optimizing[scenario_id] = True
                    observers[scenario_id] = CustomObserver()

                    op = Optimizer(connections[scenario_id])
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
                    connections.pop(scenario_id)
                    observers.pop(scenario_id)

        elif action == "init":
            if scenario_id not in connections: 
                connections[scenario_id] = websocket
            elif scenario_id in optimizing:
               print("hola")
               await asyncio.create_task(send_optimization_progress(websocket, scenario_id))

        else:
            logging.warning("Unknown action: %s", action)

       

async def main():
    async with websockets.serve(handler, "optimizer.cybiraconsulting.local", 8001):
        await asyncio.Future()


async def send_optimization_progress(websocket, scenario_id):
    ob:CustomObserver=observers[scenario_id]
    while websocket.open:
        await websocket.send(json.dumps({"action": "update", "progress": ob.porcetual_progress, "elapsed":ob.elapsed, "remaining":ob.remaining}))
        if ob.porcetual_progress == 100:
            await websocket.send(json.dumps({"exiting":True, "message": optimizing.get(scenario_id)}))
            break
        await asyncio.sleep(0.1)

if __name__ == "__main__":
    asyncio.run(main())