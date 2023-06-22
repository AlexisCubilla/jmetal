from websocket import create_connection
import json
import threading
import time


ws = create_connection("ws://localhost:8002")

auth_data = {
            'action': 'init',
            'message': 'Connection Request',
            'connId': 1
        }
ws.send(json.dumps(auth_data))

print(ws.recv())

ws.send('{"connId":1, "action":"optimize","message":{"float":{"lower_bound":[-20.0,-20.0],"upper_bound":[20.0,20.0]},"binary":{"number_of_bits":10},"stop_criteria":{"max_evaluations":3000,"max_seconds":0},"number_of_objectives":1,"directions":[-1,-1],"population":100,"offspring_population":100,"simulation_periods":100,"mutation":{"float":{"PolynomialMutation":{"probability":0.01,"distribution_index":20}},"binary":{"BitFlipMutation":{"probability":0.01}}},"crossover":{"float":{"SBXCrossover":{"probability":1.0,"distribution_index":20}},"binary":{"SPXCrossover":{"probability":1.0}}}}}')



while True:
    print(ws.recv())