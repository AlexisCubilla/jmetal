from client_ws import WsClient
import json

ws = WsClient("ws://localhost:8001")

message = {
    "method": "POST",
    "action": "get_scenario_model",
    "project_id": "65c35b37-d464-44d1-b2d5-643059f8291e",
    "scenario_id":"859ba5ec-9499-4de2-825d-cb3f78b0af79"
}
json_string = json.dumps({"action": "optimize", "message": message})

print(json_string)
objetives=ws.send_data(json_string)
print(objetives)