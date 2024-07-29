import json
from jmetal.algorithm.multiobjective.nsgaii import NSGAII
from jmetal.operator import  IntegerPolynomialMutation, PolynomialMutation, SBXCrossover, BitFlipMutation, SimpleRandomMutation, UniformMutation
from jmetal.operator.mutation import CompositeMutation
from jmetal.util.termination_criterion import StoppingByEvaluations
import numpy as np
from calibration.data import CalibrationData
from calibration.problem import CalibrationProblem
from calibration.termination_criterion import  StopByEvaluationWithRestrictions
from jmetal.operator.crossover import CompositeCrossover, IntegerSBXCrossover, SPXCrossover
from jmetal.util.observer import ProgressBarObserver
from jmetal.util.constraint_handling import is_feasible
from jmetal.core.solution import CompositeSolution
from jmetal.core.quality_indicator import FitnessValue
from typing import List

class OptimizerWithCalibration:
    def __init__(self, websocket):
        self.websocket = websocket
    
    def optimize(self, data):
        # try:
            self.data:CalibrationData = data
            self.problem = CalibrationProblem(self.data, self.websocket)
            self.mutations, self.crossovers = self.data.operators()
            self.max_evaluations = self.data.max_evaluations
            self.extra_evaluations = self.data.extra_evaluations
            self.population_size = self.data.population
            self.offspring_population_size = self.data.offspring_population
            solutions = self.run_nsgaii()

            if solutions:
                variables= self.process_results(solutions)
                
            self.websocket.send(str(json.dumps(self.buildMessage(variables))))
        
    def buildMessage(self, variables:List[float]):
        if not variables:
            message = {
                "type": "close",
                    "status": "error",
                    "message": "No feasible solution could be determined during calibration based on the provided constraints"
            }
        else:
            message = {
                "type": "close",
                "status": "success",
                "data": {
                    "inputs": [
                        {
                            "id": input["id"],
                            "parent": input["parent"],
                            "data": variable
                        }
                        for input, variable in zip(self.data.inputs, variables)
                    ]
                },
            }
        return message
        
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
        # termination_criterion=StoppingByEvaluations(max_evaluations=self.max_evaluations),
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

    def process_results(self, solutions:  List[CompositeSolution]):
        min_fitness: float = float("inf")
        final_solution_variables: List[float] = []
        if True: #if check_feasibility:
            list_of_composite_solutions: List[CompositeSolution] = [solution for solution in solutions if is_feasible(solution)]
            if list_of_composite_solutions:
                for i, composite_solution in enumerate(list_of_composite_solutions):
                    if(composite_solution.variables[0].objectives[0] < min_fitness):
                        min_fitness = composite_solution.variables[0].objectives[0]
                        final_solution_variables = composite_solution.variables[0].variables
                        print("Final Solution: ",  composite_solution.objectives[0])	           
        return final_solution_variables
    
    
if __name__ == '__main__':
    pass