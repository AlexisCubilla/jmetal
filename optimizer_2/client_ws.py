from websockets.sync.client import connect
class WsClient:
    def __init__(self, uri):
        self.uri = uri

    def send_data(self, data):
        with connect(self.uri) as websocket:
            websocket.send(str(data))
            message = websocket.recv()
            return message