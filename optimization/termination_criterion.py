# from jmetal.core.quality_indicator import QualityIndicator
# from jmetal.util.termination_criterion import TerminationCriterion
# from jmetal.util.constraint_handling import is_feasible
# class StopByEvaluationOrQualityIndicator(TerminationCriterion):
#     def __init__(self, quality_indicator: QualityIndicator, expected_value: float, degree: float, max_evaluations: int, check_feasibility: bool = False):
#         super(StopByEvaluationOrQualityIndicator, self).__init__()
#         self.quality_indicator = quality_indicator
#         self.expected_value = expected_value
#         self.degree = degree
#         self.value = 0.0
#         self.max_evaluations = max_evaluations
#         self.evaluations = 0
#         self.check_feasibility = check_feasibility
#         self.feasible = False
#     def update(self, *args, **kwargs):
#         solutions = kwargs["SOLUTIONS"]
#         self.evaluations = kwargs["EVALUATIONS"]
#         if solutions:
#             self.value += self.quality_indicator.compute(solutions)
#             if self.check_feasibility:
#                 self.feasible = any(is_feasible(solution) for solution in solutions)
#     @property
#     def is_met(self):
#         if self.quality_indicator.is_minimization:
#             quality_indicator_met = abs(self.value) * self.degree < self.expected_value
#         else:
#             quality_indicator_met = abs(self.value) * self.degree > self.expected_value

#         evaluations_met = self.evaluations >= self.max_evaluations
#         return quality_indicator_met or evaluations_met and ( self.feasible or not self.check_feasibility)
    
from jmetal.util.termination_criterion import TerminationCriterion
from jmetal.util.constraint_handling import is_feasible
class StopByEvaluationWithRestrictions(TerminationCriterion):
    def __init__(self, max_evaluations: int, extra_evaluations: int, check_feasibility: bool = False):
        super(StopByEvaluationWithRestrictions, self).__init__()
        self.max_evaluations = max_evaluations
        self.evaluations = 0
        self.extra_evaluations = extra_evaluations
        self.check_feasibility = check_feasibility
        self.feasible = False
    def update(self, *args, **kwargs):
        solutions = kwargs["SOLUTIONS"]
        self.evaluations = kwargs["EVALUATIONS"]
        if solutions and self.check_feasibility:
            self.feasible = any(is_feasible(solution) for solution in solutions)
    
    @property
    def is_met(self):
        if self.evaluations >= self.max_evaluations:
            if not self.check_feasibility or self.feasible or self.evaluations >= self.max_evaluations + self.extra_evaluations:
                return True
        return False