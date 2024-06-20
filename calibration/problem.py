import json
import random
from jmetal.core.solution import CompositeSolution, FloatSolution
from jmetal.core.problem import Problem
from calibration.data import CalibrationData


class CalibrationProblem(Problem):
    def __init__(self, data: CalibrationData, websocket):
        super(Problem, self).__init__()
        self.websocket = websocket
        self.data: CalibrationData = data

        self.message = {
            "type": "simulate",
            "data":{
                "inputs":[]
            }
        }
        
        for input in self.data.inputs:
            self.message["data"]["inputs"].append({"id": input["id"], "data": input["data"]})
            

    def evaluate(self, solution: CompositeSolution) -> CompositeSolution:
        for i, impact in enumerate(solution.variables[0].variables):
            self.message["data"]["inputs"][i]["data"] = impact
        print("ENVIANDO....", self.message)
        self.websocket.send(str(json.dumps(self.message)))
        message = self.websocket.recv()
        message_dict: dict = json.loads(message)
        print(message_dict["data"], "......RECIBIDO")
        type = message_dict["type"]
        if type == "result":
            for i in range(self.number_of_objectives()): 
                solution.objectives[i] = message_dict["data"]

        self.__evaluate_constraints([1, 2], solution)
        return solution

    def __evaluate_constraints(self, constraints, solution: CompositeSolution) -> None:
        solution.constraints[0] = constraints[0]

    def create_solution(self) -> CompositeSolution:
        solution = []
        float_solution = FloatSolution(
            self.data.lower_bound,
            self.data.upper_bound,
            self.number_of_objectives(),
            self.number_of_constraints(),
        )
        float_solution.variables = [
            random.uniform(lower, upper)
            for lower, upper in zip(self.data.lower_bound, self.data.upper_bound)
        ]

        solution.append(float_solution)
        return CompositeSolution(solution)

    def number_of_variables(self) -> int:
        return len(self.data.inputs)

    def number_of_objectives(self) -> int:
        return self.data.number_of_objectives

    def number_of_constraints(self) -> int:
        return 0

    def name(self) -> str:
        return "Calibration Problem"

    def process_message(self, message):
        message_dict: dict = json.loads(message)
        if "error" in message_dict:
            raise Exception("The simulation failed:", message_dict["error"])
        uuid: str = message_dict["result"]["uuid"]
        valor: str = message_dict["result"]["value"]
        return dict(zip(uuid, valor))
