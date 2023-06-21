from client_ws import WsClient
import json

ws = WsClient("ws://main/optimizer")

message = {
    "method": "POST",
    "action": "get_scenario_model",
    "project_id": "70f96e6a-963d-4748-b8dc-5196c848ee19",
    "scenario_id":"8de72d83-ab3b-46b6-a2ce-5f2343001031"
}
json_string = json.dumps({"action": "optimize", "message": message})

print(json_string)
objetives=ws.send_data(json_string)
print(objetives)