from client_ws import WsClient
import json

ws = WsClient("ws://localhost:8001")

int_lower_bound = [-20, -20]
int_upper_bound = [20, 20]
float_lower_bound = [-20.0, -20.0]
float_upper_bound = [20.0, 20.0]

max_evaluations = 10000

message = {
    "int": {
        "lower_bound": int_lower_bound,
        "upper_bound": int_upper_bound
    },
    "float": {
        "lower_bound": float_lower_bound,
        "upper_bound": float_upper_bound
    },
    "max_evaluations": max_evaluations,
    "number_of_objectives": 2
}

json_string = json.dumps({"action": "optimize", "message": message})


objetives=ws.send_data(json_string)
print(objetives)
