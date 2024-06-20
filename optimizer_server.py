import logging
import websockets
import asyncio
import json
from calibration.optimizer import OptimizerWithCalibration
from observer import CustomObserver
from optimizer import Optimizer
from dotenv import load_dotenv
import os
import concurrent.futures
from websockets.sync.server import serve
load_dotenv()

connections = {}
optimizing = {}
observers = {}

def resolve(msg, websocket):
    try:
        print(parsed_message)
        parsed_message = json.loads(msg)
        print(parsed_message)
        type, data = parsed_message.get("type"), parsed_message.get("data")
        
        if type == "init":
            op = OptimizerWithCalibration(websocket)
            with concurrent.futures.ThreadPoolExecutor() as executor:
                optimizing, err = executor.submit(op.optimize, data).result()
            if err:
                logging.error(err)
    except Exception as e:
        logging.error(f"Error resolving message: {e}")

def handle_websocket(websocket):
    try:
        for msg in websocket:
            resolve(msg, websocket)
    except websockets.exceptions.ConnectionClosed:
        logging.info(f'Connection closed for {websocket.remote_address}')
    finally:
        # Clean up resources, if any
        pass

def main():
    host = os.getenv("SIMULATION_WEBSOCKET_HOST")
    port = int(os.getenv("SIMULATION_WEBSOCKET_PORT"))
    with serve(handle_websocket, host, port) as server:
        server.serve_forever()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
