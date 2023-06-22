import asyncio
from jmetal.algorithm.multiobjective.nsgaii import NSGAII
from jmetal.operator import  IntegerPolynomialMutation, PolynomialMutation, SBXCrossover, BitFlipMutation, SimpleRandomMutation, UniformMutation
from jmetal.operator.mutation import CompositeMutation
from jmetal.util.termination_criterion import StoppingByEvaluations
from problem import  CustomMixedIntegerFloatBinaryProblem
from jmetal.operator.crossover import CompositeCrossover, IntegerSBXCrossover, SPXCrossover
from data import Data
from jmetal.util.observer import  ProgressBarObserver
from jmetal.util.evaluator import MultiprocessEvaluator
class Optimizer:
    def __init__(self, scenario, websocket):
        data = Data()
        data.extract_scenario_data(scenario)
        self.problem = CustomMixedIntegerFloatBinaryProblem(data,scenario, websocket )
        self.mutations, self.crossovers = data.operators()
        self.max_evaluations = data.max_evaluations
        
    def optimize(self):
        solutions = asyncio.create_task( Optimizer.run_nsgaii(self, self.problem, self.max_evaluations))
        return self.process_results(solutions)

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

    def process_results(self, solutions):
        solution= solutions[0]
        final_string = ""
        variables = solution
        print(variables)
        return final_string
    
if __name__ == '__main__':
    pass