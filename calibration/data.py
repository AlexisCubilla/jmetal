from data import Operator

class CalibrationData:
    """
    A class used to represent Calibration Data
    """

    def __init__(self):
        """
        Initialize CalibrationData with default values
        """
        self.id = "uuid"
        self.utility = "uuid"
        self.type = "calibration"
        self.periods = 10
        
        self.population = 10
        self.offspring_population = 1
        self.number_of_objectives = 1
        self.max_evaluations = 20000
        self.extra_evaluations = 300
        
        self.directions = [-1]
        self.outputs = [
            {"id": "1", "value": "13", "time": "2"},
            {"id": "2", "value": "4", "time": "12"}
        ]
        self.inputs = [
            {"id": "1", "value": "0.4"},
            {"id": "2", "value": "-0.3"}            
        ]
        
        self.impacts = [ -0.8, -0.6, -0.4, -0.2, 0, 0.2, 0.4, 0.6, 0.8 ]
        self.impacts_count = len(self.impacts)
        
        self.lower_bound = []
        self.upper_bound = []
        
        for input in self.inputs:
            if float(input['value']) > 0:
                self.lower_bound.append(0)
                self.upper_bound.append(1)
            else:
                self.lower_bound.append(-1)
                self.upper_bound.append(0)

    def operators(self) -> list:
        """
        Create and return mutation and crossover operators
        """
        mutations = []
        crossovers = []
        mutations.append(Operator("PolynomialMutation", 0.01, 20))
        crossovers.append(Operator("SBXCrossover", 1.0, 20))

        return mutations, crossovers