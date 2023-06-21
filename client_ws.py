from websockets.sync.client import connect
class WsClient:
    def __init__(self, uri):
        self.uri = uri

    def send_data(self, data):
        with connect(self.uri, open_timeout=None, close_timeout=None) as websocket:
            websocket.send(str(data))
            message = websocket.recv()
            return message

