import websockets
import asyncio
import json
from optimizer import Optimizer

connections = {}
solutions = {}
async def handler(websocket):
    while True:
        try:
            data = await asyncio.create_task( websocket.recv())
            print(data)
            parsedData = json.loads(data)
            connections[parsedData['connId']] = websocket
            print(connections)
        except websockets.ConnectionClosed as e:
            if e.code == 1006 or e.code == 1005:
                # Unexpected closure
                print('se cerro la conexion')
                break
        
        await asyncio.create_task( resolve(data, parsedData['connId']))
        #asyncio.create_task(on_message(await ws.recv()))
        #await connections[parsedData['connId']].close()    

async def resolve(data, connId):
    parsed_data = json.loads(data)
    action = parsed_data["action"]
    message = parsed_data["message"]
    global solutions
    has_int, has_float, has_binary = True, True, True
    if action == "optimize":
        if message.get("int") is None: has_int=False
        if message.get("float") is None: has_float=False
        if message.get("binary") is None: has_binary=False
        
        await connections[connId].send('se comienza la optimizacion')
        op = Optimizer(has_int, has_float, has_binary, message)
        solutions = op.optimize()
        await connections[connId].send(json.dumps(solutions))
    elif action == "reconnect":
        print('que pasa aca')
        await connections[connId].send(json.dumps(solutions))
        print('test')
    elif action == "init":
        await connections[connId].send("comunication started")
        
async def main():
    async with websockets.serve(handler, "localhost", 8002):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())