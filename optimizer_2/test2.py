from client_ws import WsClient
import json

json_string = json.dumps({"action": "restore", "message":"restore"})
ws = WsClient("ws://localhost:8001")
#print(json_string)

objetives=ws.send_data(json_string)
print(objetives)