from jmetal.algorithm.multiobjective.nsgaii import NSGAII
from jmetal.operator import  IntegerPolynomialMutation, PolynomialMutation, SBXCrossover, BitFlipMutation, SimpleRandomMutation, UniformMutation
from jmetal.operator.mutation import CompositeMutation
from jmetal.util.termination_criterion import StoppingByEvaluations
from problem import  CustomMixedIntegerFloatBinaryProblem
from jmetal.operator.crossover import CompositeCrossover, IntegerSBXCrossover, SPXCrossover
from jmetal.util.evaluator import MultiprocessEvaluator
from jmetal.util.observer import  ProgressBarObserver
import logging

LOGGER = logging.getLogger("jmetal")
class Optimizer:
    def __init__(self, has_int, has_float, has_binary, message):
        self.problem = CustomMixedIntegerFloatBinaryProblem(message, has_int, has_float, has_binary)
        self.mutations=message["mutation"]
        self.crossovers=message["crossover"]
        self.max_evaluations = message["stop_criteria"]["max_evaluations"]
        
    def optimize(self):
        solutions = Optimizer.run_nsgaii(self, self.problem, self.max_evaluations)
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
        for _, mutation_info in self.mutations.items():
            mutation_type = list(mutation_info.keys())[0]
            probability = mutation_info[mutation_type].get("probability")
            distribution_index = mutation_info[mutation_type].get("distribution_index")
            perturbation = mutation_info.get("perturbation")
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
        for _, crossover_info in self.crossovers.items():
                crossover_type = list(crossover_info.keys())[0]
                probability = crossover_info[crossover_type].get("probability")
                distribution_index = crossover_info[crossover_type].get("distribution_index")
                crossover_kwargs = {
                    "probability": probability
                }
                if distribution_index is not None:
                    crossover_kwargs["distribution_index"] = distribution_index
                crossover_list.append(mapped_crossover_functions[crossover_type](**crossover_kwargs))
        return crossover_list


    def run_nsgaii(self, problem, max_evaluations):
        algorithm = NSGAII(
            population_evaluator=MultiprocessEvaluator(32),
            problem=problem,
            population_size=100,
            offspring_population_size=100,
            mutation=CompositeMutation(self.mutation()),
            crossover=CompositeCrossover(self.crossover()),
            termination_criterion=StoppingByEvaluations(max_evaluations=max_evaluations),
        )
        progress_bar = ProgressBarObserver(max=max_evaluations)
        algorithm.observable.register(progress_bar)
        algorithm.run()
        LOGGER.debug("execution time: %s",algorithm.total_computing_time)
        # print("Tiempo de ejecucion del algoritmo: ---------------->",)
        solutions = algorithm.get_result() 
        return solutions

    def process_results(self, solutions):
        solution= solutions[0]
        final_string = ""
        variables = solution.variables[0].variables + solution.variables[1].variables
        # print(variables)
        return variables
    
if __name__ == '__main__':
    pass