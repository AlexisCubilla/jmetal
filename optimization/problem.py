import json
import random
from jmetal.core.solution import CompositeSolution, FloatSolution, IntegerSolution, BinarySolution
from jmetal.core.problem import Problem
from optimization.data import OptimizationData


class OptimizationProblem(Problem):
    def __init__(self, data: OptimizationData, websocket):
        super(Problem, self).__init__()
        self.websocket = websocket
        self.data: OptimizationData = data
        
        
        self.message = {
            "model_id": self.data.simulation_model_id,
            "periods": self.data.simulation_periods,
            "iterations": self.data.simulation_iterations,
            "inputs":[]
        }
        
        for input in self.data.inputs:
            self.message["inputs"].append({"id": input["id"], "value": input["data"]})
            

    def evaluate(self, solution: CompositeSolution) -> CompositeSolution:
        uuid_dicts = {
                    int: self.data.int_uuid,
                    float: self.data.float_uuid,
                    bool: self.data.binary_uuid
                }
        for i in solution.variables:
            var_type = type(i.variables[0])
            uuid_dict = uuid_dicts.get(var_type, self.data.binary_uuid)
            
            for j, value in enumerate(i.variables):
                self.message["inputs"][j]["id"] = uuid_dict[j]
                self.message["inputs"][j]["value"] = value

        self.websocket.send(str(json.dumps(self.message)))
        message = self.websocket.recv()
        message_dict: dict = json.loads(message)
        for i, value in enumerate(message_dict["value"]):
            solution.objectives[i] = value

        # self.__evaluate_constraints([1, 2], solution)
        
        return solution

    def __evaluate_constraints(self, constraints, solution: CompositeSolution) -> None:
        solution.constraints[0] = constraints[0]

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
        return len(self.data.inputs)

    def number_of_objectives(self) -> int:
        return self.data.number_of_objectives

    def number_of_constraints(self) -> int:
        return 0

    def name(self) -> str:
        return "Optimization Problem"

    def process_message(self, message):
        message_dict: dict = json.loads(message)
        if "error" in message_dict:
            raise Exception("The simulation failed:", message_dict["error"])
        uuid: str = message_dict["result"]["uuid"]
        valor: str = message_dict["result"]["value"]
        return dict(zip(uuid, valor))
