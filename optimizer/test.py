from client_ws import WsClient
import json

ws = WsClient("ws://localhost:8001")

lower_bound_list = [-20, -20]
upper_bound_list = [20, 20]
max_evaluations = 1000

message = {
    "variable": {
        "lower_bound_list": lower_bound_list,
        "upper_bound_list": upper_bound_list
    },
    "max_evaluations": max_evaluations
}

json_string = json.dumps({"action": "optimize", "message": message})


objetives=ws.send_data(json_string)
print(objetives)
