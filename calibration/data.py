import json
from data import Operator

class CalibrationData:
    """
    A class used to represent Calibration Data
    """

    def __init__(self, data=None):
     
        self.population = 10
        self.offspring_population = 1
        self.number_of_objectives = 1
        self.max_evaluations = 200
        self.extra_evaluations = 1
        self.strict_constraint_verification = False
        self.directions = [-1]
        self.inputs = [
        ]
        
        self.lower_bound = []
        self.upper_bound = []
        if data:
            self.load_data(data)
            self.setBounds()
        self.print()

        
    def load_data(self, data):
        try:
            self.number_of_constraints = data.get("constraints", 0)
            
            model = data.get("model", {})
            self.population = model.get("population", 10)
            self.offspring_population = model.get("offspring", 1)
            self.max_evaluations = model.get("maxEvaluations", 200)
            self.extra_evaluations = model.get("extraEvaluations", 0)
            self.strict_constraint_verification = model.get("strictConstraints", False)
            
            inputs = data.get("inputs", [])
            for input_data in inputs:
                id = input_data.get("id")
                default_num = json.loads(input_data.get("metadata", {}).get("default", "{}")).get("num")
                self.inputs.append({"id": id, "data": default_num})
            else:
                raise ValueError("Invalid message type. Expected 'init'.")
            
                
        except Exception as e:
            print(f"Error loading inputs from JSON: {e}")
        print(f"Loaded inputs: {self.inputs}")
    
    
    def setBounds(self):
        for input in self.inputs:
            if float(input['data']) > 0:
                
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
    
    def print(self) -> None:
        print(f"population: {self.population}")
        print(f"offspring_population: {self.offspring_population}")
        print(f"number_of_objectives: {self.number_of_objectives}")
        print(f"max_evaluations: {self.max_evaluations}")
        print(f"extra_evaluations: {self.extra_evaluations}")
        print(f"strict_constraint_verification: {self.strict_constraint_verification}")
        print(f"directions: {self.directions}")
        print(f"inputs: {self.inputs}")
        print(f"lower_bound: {self.lower_bound}")
        print(f"upper_bound: {self.upper_bound}")
        print(f"number_of_constraints: {self.number_of_constraints}")
        