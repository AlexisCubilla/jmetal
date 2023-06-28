import json
from websockets.sync.client import connect


with connect("ws://main/optimizer", open_timeout=None, close_timeout=None) as websocket:
    message = {
    "action": "init",
    "project_id": "bb438245-4b48-4864-8854-0810ec92e509",
    "scenario_id": "be88c852-55d3-4baa-aad7-499c45dd837e"
    }
    json_string = json.dumps(message)

    print(json_string)
    websocket.send(str(json_string))

    message = {
    "action": "optimize",
    "project_id": "bb438245-4b48-4864-8854-0810ec92e509",
    "scenario_id": "be88c852-55d3-4baa-aad7-499c45dd837e"
    }
    json_string = json.dumps(message)

    print(json_string)
    websocket.send(str(json_string))
    while True:
        print("waiting for message")
        objectives = websocket.recv()
        print(objectives)

