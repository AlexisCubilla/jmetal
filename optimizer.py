import json
from jmetal.algorithm.multiobjective.nsgaii import NSGAII
from jmetal.operator import  IntegerPolynomialMutation, PolynomialMutation, SBXCrossover, BitFlipMutation, SimpleRandomMutation, UniformMutation
from jmetal.operator.mutation import CompositeMutation
from jmetal.util.termination_criterion import StoppingByEvaluations
from database import Database
from observer import CustomObserver
from problem import  CustomMixedIntegerFloatBinaryProblem
from jmetal.operator.crossover import CompositeCrossover, IntegerSBXCrossover, SPXCrossover
from data import Data
from websockets.sync.client import connect

class Optimizer:
    def __init__(self, websocket):
        self.websocket = websocket
    
    def optimize(self, scenario_id, project_id, observer:CustomObserver):
        try:
             with connect("ws://sim.cybiraconsulting.local:8001", open_timeout=None, close_timeout=None) as websocket:
                message = {"action": "init","id": scenario_id,"project_id": project_id}
                websocket.send(str(json.dumps(message)))           
                while True:
                    message = websocket.recv()
                    if "message" in message:
                        break
                
                db = Database()
                scenario = db.get_scenario(project_id, scenario_id)    
                data = Data()
                data.extract_scenario_data(scenario)
                # lista= data.check_empty_parameters()
                self.problem = CustomMixedIntegerFloatBinaryProblem(data, websocket)
                
                self.mutations, self.crossovers = data.operators()
                self.max_evaluations = data.max_evaluations
                self.population_size = data.population
                self.offspring_population_size = data.offspring_population
                
                solutions = self.run_nsgaii(observer)

                if solutions:
                    variables= self.process_results(solutions, data)
                    db.save_optimized_variables(scenario, variables)
                return variables, None
             
        except Exception as e:
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


    def run_nsgaii(self, observer:CustomObserver):
        algorithm = NSGAII(
            problem=self.problem,
            population_size=self.population_size,
            offspring_population_size=self.offspring_population_size,
            mutation=CompositeMutation(self.mutation()),
            crossover=CompositeCrossover(self.crossover()),
        termination_criterion=StoppingByEvaluations(max_evaluations=self.max_evaluations),
        )
        observer.set_max(self.max_evaluations)
        algorithm.observable.register(observer)
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