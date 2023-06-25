from client_ws import WsClient
import json

ws = WsClient("ws://main/optimizer")

message = {
    "method": "POST",
    "project_id": "a40c3013-eb9a-44c3-bfe8-8e1af32e40cf",
    "scenario_id":"3c073387-7b13-4fd9-945e-16ddb44c1544"
}
json_string = json.dumps({"action": "optimize", "message": message})

print(json_string)
objetives=ws.send_data(json_string)
print(objetives)