import json
from jmetal.algorithm.multiobjective.nsgaii import NSGAII
from jmetal.operator import  IntegerPolynomialMutation, PolynomialMutation, SBXCrossover, BitFlipMutation, SimpleRandomMutation, UniformMutation
from jmetal.operator.mutation import CompositeMutation
from optimization.data import OptimizationData
from optimization.problem import OptimizationProblem
from optimization.termination_criterion import  StopByEvaluationWithRestrictions
from jmetal.operator.crossover import CompositeCrossover, IntegerSBXCrossover, SPXCrossover
from jmetal.util.observer import ProgressBarObserver
from jmetal.core.solution import CompositeSolution
from typing import List

class Optimizer:
    def __init__(self, websocket):
        self.websocket = websocket
    
    def optimize(self, data: OptimizationData):
        self.data = data
        self.problem = OptimizationProblem(self.data, self.websocket)
        self.mutations, self.crossovers = self.data.operators()
        self.max_evaluations = self.data.max_evaluations
        self.extra_evaluations = self.data.extra_evaluations
        self.population_size = self.data.population
        self.offspring_population_size = self.data.offspring_population
        solutions = self.run_nsgaii()
        if solutions:
            variables: dict= self.process_results(solutions)
            for key, value in variables.items():
                print("key ",key, "value", value)
        
        self.websocket.send(str(json.dumps(variables)))

        
    # def build_message(self, composite_solutions_list: List[CompositeSolution]):
    #     message = {
    #         "type": "close",
    #         "data": {
    #             "inputs": [
    #                 {
    #                     "id": input["id"],
    #                     "parent": input["parent"],
    #                     "data": solution.variables
    #                 }
    #                 for input, solution in zip(self.data.objective_uuid, solutions)
    #             ]
    #         }
    #     }
    #     return "hola"
        
    def mutation(self):
        mapped_mutation_functions = {
                        "IntegerPolynomialMutation": IntegerPolynomialMutation,
                        "PolynomialMutation": PolynomialMutation,
                        "SimpleRandomMutation": SimpleRandomMutation,
                        "UniformMutation": UniformMutation,
                        "BitFlipMutation": BitFlipMutation
        }
        mutation_list=[]
        for mutation in self.mutations:
            mutation_type = mutation.name
            probability =   mutation.probability
            distribution_index = mutation.distribution_index
            perturbation = None #mutation.get("perturbation")
            if probability is not None:
                if distribution_index is not None:
                    mutation_kwargs = {
                        "probability": probability,
                        "distribution_index": distribution_index
                    }
                elif perturbation is not None:
                    mutation_kwargs = {
                        "probability": probability,
                        "perturbation": perturbation
                    }
                else:
                    mutation_kwargs = {
                        "probability": probability
                    }
                mutation_list.append(mapped_mutation_functions[mutation_type](**mutation_kwargs))
        return mutation_list


    def crossover(self):
        mapped_crossover_functions = {
            "IntegerSBXCrossover": IntegerSBXCrossover,
            "SBXCrossover": SBXCrossover,
            "SPXCrossover": SPXCrossover
        }
        crossover_list = []
        for crossover in self.crossovers:
            crossover_type = crossover.name
            probability = crossover.probability
            distribution_index = crossover.distribution_index
            crossover_kwargs = {
                "probability": probability
            }
            if distribution_index is not None:
                crossover_kwargs["distribution_index"] = distribution_index
            crossover_list.append(mapped_crossover_functions[crossover_type](**crossover_kwargs))
        return crossover_list


    def run_nsgaii(self):
        algorithm = NSGAII(
            problem=self.problem,
            population_size=self.population_size,
            offspring_population_size=self.offspring_population_size,
            mutation=CompositeMutation(self.mutation()),
            crossover=CompositeCrossover(self.crossover()),
            termination_criterion=StopByEvaluationWithRestrictions( 
                                                                     max_evaluations=self.max_evaluations,
                                                                     extra_evaluations=self.extra_evaluations,
                                                                     check_feasibility=True),
        )
        observer = ProgressBarObserver(self.max_evaluations)
        algorithm.observable.register(observer)
        algorithm.run()
        solutions = algorithm.get_result()
        return solutions

    def process_results(self, composite_solutions_list: List[CompositeSolution]):
        def process_solution(solution, uuid_list):
            if len(solution) != len(uuid_list):
                print(solution, uuid_list)
                raise ValueError("Length of solution and uuid_list must match")
            return [{"id": uuid, "value": value} for uuid, value in zip(uuid_list, solution)]
        composite_solution_map = {}
        for index, composite_solutions in enumerate(composite_solutions_list):
            uuid_value_pairs = []
            for solutions in composite_solutions.variables:
                if isinstance(solutions.variables[0], int):
                    uuid_value_pairs.extend(process_solution(solutions.variables, self.data.int_uuid))
                elif isinstance(solutions.variables[0], float):
                    uuid_value_pairs.extend(process_solution(solutions.variables, self.data.float_uuid))
                else:
                    uuid_value_pairs.extend(process_solution(solutions.variables[0], self.data.binary_uuid))
            composite_solution_map[index] = uuid_value_pairs  
        return composite_solution_map
if __name__ == '__main__':
    pass