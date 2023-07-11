
from jmetal.util.observer import Observer
from tqdm import tqdm
class CustomObserver(Observer):
    def __init__(self):
        self.progress_bar = None
        self.progress = 0
        self._max = 0
        self._porcetual_progress=0
        self._elapsed=0
        self._remaining=0
        self._elapsed_str=""
        self._remaining_str=""

    def update(self, *args, **kwargs):
        evaluations = kwargs["EVALUATIONS"]
        
        if not self.progress_bar:
            self.progress_bar = tqdm(total=self._max, ascii=True, desc="Progress")

        self.progress_bar.update(evaluations - self.progress)
        self.progress = evaluations

        if self.progress >= self._max:
            self.progress_bar.close()

        #enviar un valor de 0 a 100 que represente el progreso de la optimización
        self._porcetual_progress= int((evaluations/self._max)*100)

        elapsed= self.progress_bar.format_dict["elapsed"]
        total= self.progress_bar.format_dict["total"]
        n= self.progress_bar.format_dict["n"]
        rate = self.progress_bar.format_dict["rate"]
        remaining = (total - n) / rate if rate and self.progress_bar.total else 0

        self._remaining_str = self.progress_bar.format_interval(remaining)
        self._elapsed_str = self.progress_bar.format_interval(elapsed)
    @property
    def porcetual_progress(self):
        return self._porcetual_progress

    @property
    def elapsed(self):
        return self._elapsed_str
    
    @property
    def remaining(self):
        return self._remaining_str
    
    def set_max(self, max:int):
        self._max = max