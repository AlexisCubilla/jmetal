import asyncio
import json
from jmetal.algorithm.multiobjective.nsgaii import NSGAII
from jmetal.operator import  IntegerPolynomialMutation, PolynomialMutation, SBXCrossover, BitFlipMutation, SimpleRandomMutation, UniformMutation
from jmetal.operator.mutation import CompositeMutation
from jmetal.util.termination_criterion import StoppingByEvaluations
import requests
from database import Database
from problem import  CustomMixedIntegerFloatBinaryProblem
from jmetal.operator.crossover import CompositeCrossover, IntegerSBXCrossover, SPXCrossover
from data import Data
from jmetal.util.observer import  ProgressBarObserver
from jmetal.util.evaluator import MultiprocessEvaluator
url_pg="http://sim.cybiraconsulting.local:3001"

class Optimizer:
    
    def optimize(self, scenario, websocket):
        try:
            data = Data()
            data.extract_scenario_data(scenario)
            self.problem = CustomMixedIntegerFloatBinaryProblem(data, scenario, websocket)
            self.mutations, self.crossovers = data.operators()
            self.max_evaluations = data.max_evaluations
            self.population_size = data.population
            self.offspring_population_size = data.offspring_population
            
            solutions = self.run_nsgaii(self.problem, self.max_evaluations)

            if solutions:
                result= self.process_results(solutions, data)
                db=Database()
                db.save_scenario(scenario, result)
            return result, None
        
        except Exception as e:
            print(e)
            return None, e
        

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


    def run_nsgaii(self, problem, max_evaluations):
        algorithm = NSGAII(
            problem=problem,
            population_size=1,
            offspring_population_size=1,
            mutation=CompositeMutation(self.mutation()),
            crossover=CompositeCrossover(self.crossover()),
        termination_criterion=StoppingByEvaluations(max_evaluations=max_evaluations),
        )
        progress_bar = ProgressBarObserver(max=max_evaluations)
        algorithm.observable.register(progress_bar)
        algorithm.run()
        solutions = algorithm.get_result() 
        return solutions

    def process_results(self, solutions, data:Data):
        processed_result = {} 
        uuids = []
        values = []
        for i in solutions[0].variables:
            if(isinstance(i.variables[0], int)):
                uuids+=data.int_uuid
                values+=i.variables
            elif(isinstance(i.variables[0], float)):
                uuids+=data.float_uuid
                values+=i.variables
            else:
                uuids+=data.binary_uuid
                values+=i.variables[0]
        
        processed_result = dict(zip(uuids, values))
        print(processed_result)
        return processed_result
    
    
if __name__ == '__main__':
    pass