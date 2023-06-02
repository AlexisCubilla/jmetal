import random
from jmetal.core.solution import (CompositeSolution,FloatSolution,IntegerSolution,BinarySolution)
from jmetal.core.problem import (Problem)
from client_ws import WsClient

class CustomMixedIntegerFloatProblem(Problem):


    def __init__(self):
        super(CustomMixedIntegerFloatProblem, self).__init__()
        self.float_lower_bound = []
        self.float_upper_bound = []
        self.int_lower_bound = []
        self.int_upper_bound = []
        self.number_of_bits=0
        self.number_of_objectives_count = 0
        # self.obj_directions = [self.MINIMIZE]
        # self.obj_labels = ["Ones"]

    def evaluate(self, solution: CompositeSolution) -> CompositeSolution:
        ws = WsClient("ws://localhost:8000")
        message={}
        for i in solution.variables:   
            if(isinstance(i.variables[0], int)):
                message["int"]=i.variables
            elif(isinstance(i.variables[0], float)):
                message["float"]=i.variables
            else:
                message["binary"]=i.variables
        objetives=eval(ws.send_data(str(message)))

        for i in range(self.number_of_objectives()):
            solution.objectives[i] = objetives[i]
        return solution

    def create_solution(self) -> CompositeSolution:
        integer_solution = IntegerSolution(
            self.int_lower_bound, self.int_upper_bound, self.number_of_objectives(), self.number_of_constraints()
        )
        float_solution = FloatSolution(
            self.float_lower_bound, self.float_upper_bound, self.number_of_objectives(), self.number_of_constraints()
        )
        binary_solution = BinarySolution(
            1, self.number_of_objectives(), self.number_of_constraints()
        )

        float_solution.variables = [
            random.uniform(self.float_lower_bound[i] * 1.0, self.float_upper_bound[i] * 1.0)
            for i in range(len(self.float_lower_bound))
        ]
        integer_solution.variables = [
            random.randint(self.int_lower_bound[i], self.int_upper_bound[i])
            for i in range(len(self.int_lower_bound))
        ]

        binary_solution.variables[0] = [
        True if random.randint(0, 1) == 0 else False for _ in range(self.number_of_bits)
        ]

        return CompositeSolution([integer_solution, float_solution, binary_solution])
    
 
    def number_of_variables(self) -> int:
        return len(self.float_lower_bound) + len(self.int_lower_bound)

    def number_of_objectives(self) -> int:
        return self.number_of_objectives_count

    def number_of_constraints(self) -> int:
        return 0
    
    def name(self) -> str:
        return "Mixed Integer Float Problem"