import json
import random
from jmetal.core.solution import (CompositeSolution,FloatSolution,IntegerSolution,BinarySolution)
from jmetal.core.problem import (Problem)
from client_ws import WsClient
from data import Data
class CustomMixedIntegerFloatBinaryProblem(Problem):

    def __init__(self, data: Data, websocket):
        super(CustomMixedIntegerFloatBinaryProblem, self).__init__()
        self.websocket = websocket
        self.data = data
        # self.obj_labels = ["Ones"]

        self.message = {
            "action": "optimize",
            "message": {
                "variables": {
                    "uuids": [],
                    "values": []
                }
            }
        }

    def evaluate(self, solution: CompositeSolution) -> CompositeSolution:
        uuids=[]
        values=[]
        objetives=[]

        for i in solution.variables:   
            if(isinstance(i.variables[0], int)):
                uuids+=self.data.int_uuid
                values+=i.variables
            elif(isinstance(i.variables[0], float)):
                uuids+=self.data.float_uuid
                values+=i.variables
            else:
                uuids+=self.data.binary_uuid
                values+=i.variables[0]

        self.message["message"]["variables"]["uuids"]=uuids
        self.message["message"]["variables"]["values"]=values

        self.websocket.send(str(json.dumps(self.message)))
        message = self.websocket.recv()
        uuid_valor_dict = self.process_message(message)

        for uuid in self.data.function_uuid:
            valor = uuid_valor_dict.get(uuid)
            if valor is not None:
                objetives.append(valor)
        for i in range(self.number_of_objectives()):
            # according to the documentation diretions-> -1: Minimize, 1: Maximize, the evaluation asumes minimization so 
            # -1*-1 takes the minimization as the default
            solution.objectives[i] = -1.0*self.data.directions[i]*objetives[i]
        return solution

    def create_solution(self) -> CompositeSolution:
        solution=[]
        if self.data.has_int:
            integer_solution = IntegerSolution(
                self.data.int_lower_bound, self.data.int_upper_bound, self.number_of_objectives(), self.number_of_constraints()
            )
            integer_solution.variables = [
                random.randint(self.data.int_lower_bound[i], self.data.int_upper_bound[i])
                for i in range(len(self.data.int_lower_bound))
            ]
            solution.append(integer_solution)
        if self.data.has_float:
            float_solution = FloatSolution(
                self.data.float_lower_bound, self.data.float_upper_bound, self.number_of_objectives(), self.number_of_constraints()
            )
            float_solution.variables = [
                random.uniform(self.data.float_lower_bound[i] * 1.0, self.data.float_upper_bound[i] * 1.0)
                for i in range(len(self.data.float_lower_bound))
            ]
            solution.append(float_solution)

        if self.data.has_binary:
            binary_solution = BinarySolution(
                1, self.number_of_objectives(), self.number_of_constraints())
            binary_solution.variables[0] = [
                True if random.randint(0, 1) == 0 else False for _ in range(self.data.number_of_bits)
                ]
            solution.append(binary_solution)

        return CompositeSolution(solution)
    
    def number_of_variables(self) -> int:
        return int(self.data.has_int) + int(self.data.has_float) + int(self.data.has_binary)

    def number_of_objectives(self) -> int:
        return self.data.number_of_objectives

    def number_of_constraints(self) -> int:
        return 0
    
    def name(self) -> str:
        return "Mixed Integer Float Binary Problem"
    
    def process_message(self, message):
        message_dict: dict = json.loads(message)
        if "error" in message_dict:
            raise Exception("The simulation failed:", message_dict["error"])
        uuid: str= message_dict["result"]["uuid"]
        valor: str= message_dict["result"]["value"]
        return dict(zip(uuid, valor))
