import json
import random
from jmetal.core.solution import (CompositeSolution,FloatSolution,IntegerSolution,BinarySolution)
from jmetal.core.problem import (Problem)
from client_ws import WsClient
from data import Data
class CustomMixedIntegerFloatBinaryProblem(Problem):

    def __init__(self, data: Data, scenario, websocket):
        super(CustomMixedIntegerFloatBinaryProblem, self).__init__()
        self.websocket = websocket
        self.int_uuid=data.int_uuid
        self.float_uuid=data.float_uuid
        self.binary_uuid=data.binary_uuid
        self.function_uuid=data.function_uuid
        self.directions=data.directions
        self._number_of_objectives = data.number_of_objectives
        if data.has_int:
            self.int_lower_bound = data.int_lower_bound
            self.int_upper_bound = data.int_upper_bound
        if data.has_float:
            self.float_lower_bound = data.float_lower_bound
            self.float_upper_bound = data.float_upper_bound
        if data.has_binary:
            self.number_of_bits = data.number_of_bits

        self.has_int=data.has_int
        self.has_float=data.has_float
        self.has_binary=data.has_binary
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
                uuids+=self.int_uuid
                values+=i.variables
            elif(isinstance(i.variables[0], float)):
                uuids+=self.float_uuid
                values+=i.variables
            else:
                uuids+=self.binary_uuid
                values+=i.variables[0]
        self.message["message"]["variables"]["uuids"]=uuids
        self.message["message"]["variables"]["values"]=values
        self.websocket.send(str(json.dumps(self.message)))
        receive=self.receive_message("result")
        receive_dict=json.loads(receive)
        uuid= receive_dict["result"]["uuid"]
        valor= receive_dict["result"]["value"]
        uuid_valor_dict = dict(zip(uuid, valor))
        for uuid in self.function_uuid:
            valor = uuid_valor_dict.get(uuid)
            if valor is not None:
                objetives.append(valor)
        for i in range(self.number_of_objectives()):
            # according to the documentation diretions-> -1: Minimize, 1: Maximize, the evaluation asumes minimization so 
            # -1*-1 takes the minimization as the default
            solution.objectives[i] = -1.0*self.directions[i]*objetives[i]
        return solution

    def create_solution(self) -> CompositeSolution:
        solution=[]
        if self.has_int:
            integer_solution = IntegerSolution(
                self.int_lower_bound, self.int_upper_bound, self.number_of_objectives(), self.number_of_constraints()
            )
            integer_solution.variables = [
                random.randint(self.int_lower_bound[i], self.int_upper_bound[i])
                for i in range(len(self.int_lower_bound))
            ]
            solution.append(integer_solution)
        if self.has_float:
            float_solution = FloatSolution(
                self.float_lower_bound, self.float_upper_bound, self.number_of_objectives(), self.number_of_constraints()
            )
            float_solution.variables = [
                random.uniform(self.float_lower_bound[i] * 1.0, self.float_upper_bound[i] * 1.0)
                for i in range(len(self.float_lower_bound))
            ]
            solution.append(float_solution)

        if self.has_binary:
            binary_solution = BinarySolution(
                1, self.number_of_objectives(), self.number_of_constraints())
            binary_solution.variables[0] = [
                True if random.randint(0, 1) == 0 else False for _ in range(self.number_of_bits)
                ]
            solution.append(binary_solution)

        return CompositeSolution(solution)
    
    def number_of_variables(self) -> int:
        return len(self.float_lower_bound) + len(self.int_lower_bound) + self.number_of_bits

    def number_of_objectives(self) -> int:
        return self._number_of_objectives

    def number_of_constraints(self) -> int:
        return 0
    
    def name(self) -> str:
        return "Mixed Integer Float Binary Problem"
    

    def receive_message(self, condition):
        while True:
            message = self.websocket.recv()
            if condition in message:
                break
        return message