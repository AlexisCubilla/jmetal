import random
from jmetal.core.solution import (CompositeSolution,FloatSolution,IntegerSolution,)
from jmetal.core.problem import (Problem)
from client_ws import WsClient

class CustomMixedIntegerFloatProblem(Problem):


    def __init__(self):
        super(CustomMixedIntegerFloatProblem, self).__init__()
        self.float_lower_bound = []
        self.float_upper_bound = []
        self.int_lower_bound = []
        self.int_upper_bound = []
        self.number_of_objectives_count = 0
        # self.obj_directions = [self.MINIMIZE]
        # self.obj_labels = ["Ones"]

    def evaluate(self, solution: CompositeSolution) -> CompositeSolution:
        ws = WsClient("ws://localhost:8000")
        a=solution.variables[0].variables
        b=solution.variables[1].variables
        c=str(a+b)
        objetives=eval(ws.send_data(c))

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

        float_solution.variables = [
            random.uniform(self.float_lower_bound[i] * 1.0, self.float_upper_bound[i] * 1.0)
            for i in range(len(self.float_lower_bound))
        ]
        integer_solution.variables = [
            random.randint(self.int_lower_bound[i], self.int_upper_bound[i])
            for i in range(len(self.int_lower_bound))
        ]
        print(integer_solution.variables)

        return CompositeSolution([integer_solution, float_solution])
    
 
    def number_of_variables(self) -> int:
        return len(self.float_lower_bound) + len(self.int_lower_bound)

    def number_of_objectives(self) -> int:
        return self.number_of_objectives_count

    def number_of_constraints(self) -> int:
        return 0
    
    def name(self) -> str:
        return "Mixed Integer Float Problem"