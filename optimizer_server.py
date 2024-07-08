import logging
import websockets
import asyncio
import json
from calibration.data import CalibrationData
from calibration.optimizer import OptimizerWithCalibration
from dotenv import load_dotenv
import os
import concurrent.futures
from websockets.sync.server import serve

from optimization.data import OptimizationData
from optimization.optimizer import Optimizer
load_dotenv()

connections = {}
optimizing = {}
observers = {}

def resolve(msg, websocket):
    try:
        parsed_message = json.loads(msg)
        if parsed_message.get("type") == "init":
            op = OptimizerWithCalibration(websocket)
            data = CalibrationData(parsed_message)
        elif parsed_message.get("type") == "optimization":
            parsed_message = parsed_message[0]
            op = Optimizer(websocket)
            data = OptimizationData(parsed_message)
        else:
            logging.error("Invalid message type")
            return
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.submit(op.optimize, data).result()
    except Exception as e:
        logging.error(f"Error: {e}")

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
    try:
        host = os.getenv("SIMULATION_WEBSOCKET_HOST")
        port = int(os.getenv("SIMULATION_WEBSOCKET_PORT"))
        with serve(handle_websocket, host, port) as server:
            server.serve_forever()
            print(f"Server started on {host}:{port}")
    except KeyboardInterrupt:
        print("Server stopped by user. Exiting...")
        return


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
