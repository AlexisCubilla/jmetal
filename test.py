from client_ws import WsClient
import json

ws = WsClient("ws://main/optimizer")

message = {
"action": "optimize",
"project_id": "bb438245-4b48-4864-8854-0810ec92e509",
"scenario_id": "be88c852-55d3-4baa-aad7-499c45dd837e"
}
json_string = json.dumps(message)

print(json_string)
objetives=ws.send_data(json_string)
print(objetives)

