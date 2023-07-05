import asyncio
import json
import threading
from jmetal.util.observer import Observer
from tqdm import tqdm
class WebSocketObserver(Observer):
    def __init__(self, websocket, max:int):
        self.websocket = websocket
        self.progress_bar = None
        self.progress = 0
        self._max = max

    def update(self, *args, **kwargs):
        # Aquí puedes enviar los datos a través del websocket
        # utilizando el objeto self.websocket
        evaluations = kwargs["EVALUATIONS"]
        
        if not self.progress_bar:
            self.progress_bar = tqdm(total=self._max, ascii=True, desc="Progress")

        self.progress_bar.update(evaluations - self.progress)
        self.progress = evaluations

        if self.progress >= self._max:
            self.progress_bar.close()

        #enviar un valor de 0 a 100 que represente el progreso de la optimización
        progress= int((evaluations/self._max)*100)


        message = {"action": "update", "progress": progress}
        asyncio.run(self.websocket.send(json.dumps(message)))