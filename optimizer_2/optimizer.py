from jmetal.algorithm.multiobjective.nsgaii import NSGAII
from jmetal.operator import  IntegerPolynomialMutation, PolynomialMutation, SBXCrossover
from jmetal.operator.mutation import CompositeMutation
from jmetal.util.termination_criterion import StoppingByEvaluations
from problem import  CustomMixedIntegerFloatProblem
from jmetal.operator.crossover import CompositeCrossover, IntegerSBXCrossover

class Optimizer:
    def __init__(self):
        pass


    def optimize(self, int_lower_bound, int_upper_bound, float_lower_bound, float_upper_bound, max_evaluations, number_of_objectives):
        problem = CustomMixedIntegerFloatProblem()
        
        problem.number_of_objectives_count=number_of_objectives
        problem.int_lower_bound=int_lower_bound
        problem.int_upper_bound=int_upper_bound
        problem.float_lower_bound=float_lower_bound
        problem.float_upper_bound=float_upper_bound

        solutions = Optimizer.run_nsgaii(problem, max_evaluations)
        return self.process_results(solutions)

    def run_nsgaii(problem, max_evaluations):
        algorithm = NSGAII(
            problem=problem,
            population_size=100,
            offspring_population_size=100,
            mutation=CompositeMutation([IntegerPolynomialMutation(0.01, 20), PolynomialMutation(0.01, 20.0)]),
            crossover=CompositeCrossover(
            [
                IntegerSBXCrossover(probability=1.0, distribution_index=20),
                SBXCrossover(probability=1.0, distribution_index=20),
            ]
        ),
        termination_criterion=StoppingByEvaluations(max_evaluations=max_evaluations),
        )

        algorithm.run()
        solutions = algorithm.get_result() 
        return solutions

    def process_results(self, solutions):
        solution= solutions[0]
        final_string = ""
        variables = solution.variables[0].variables + solution.variables[1].variables
        print(variables)
        return final_string
    
if __name__ == '__main__':
    pass