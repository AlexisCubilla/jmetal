from jmetal.algorithm.multiobjective.nsgaii import NSGAII
from jmetal.operator import SBXCrossover, PolynomialMutation
from jmetal.problem import ZDT1
from jmetal.util.termination_criterion import StoppingByEvaluations
from jmetal.lab.visualization.plotting import Plot
from jmetal.util.solution import get_non_dominated_solutions
from problem import CustomProblem

class Optimizer:
    def __init__(self):
        pass


    def optimize(self, lower_bound_list, upper_bound_list, max_evaluations,number_of_objectives):
        problem = CustomProblem()\
        .set_name("Problem Name Template")\
        
        for i in range(len(lower_bound_list)):
            problem.add_variable(lower_bound_list[i], upper_bound_list[i])
        
        problem.objetives_count=number_of_objectives
        solutions = Optimizer.run_nsgaii(problem, max_evaluations)
        return solutions

    def run_nsgaii(problem, max_evaluations):
        algorithm = NSGAII(
            problem=problem,
            population_size=100,
            offspring_population_size=100,
            mutation=PolynomialMutation(probability=1.0 / problem.number_of_variables(), distribution_index=20),
            crossover=SBXCrossover(probability=1.0, distribution_index=20),
            termination_criterion=StoppingByEvaluations(max_evaluations)
        )

        algorithm.run()
        solutions = algorithm.get_result() 
        return solutions

    def process_results(self, solutions):
        solution = solutions[-1]
        parts = []

        parts.append("Objetivo")

        for obj in solution.objectives:
            parts.append(str(obj) + "\n")

        parts.append("Variables")

        for var in solution.variables:
            parts.append(str(var) + "\n")

        final_string = "".join(parts)

        return final_string
    
if __name__ == '__main__':
    problem = CustomProblem()\
    .set_name("Sum of two values")\
    .add_variable(-20.0, 20.0)\
    .add_variable(-20.0, 20.0)\

    problem.objetives_count=1

    max_evaluations = 1000
    solutions = Optimizer.run_nsgaii(problem, max_evaluations)   
    print(Optimizer.process_results(solutions))