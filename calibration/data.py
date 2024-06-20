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
        
        self.directions = [-1]
        self.inputs = [
        ]
        
        self.lower_bound = []
        self.upper_bound = []
        
        if data:
            self.load_data(data)

    def load_data(self, data):
        try:
            inputs = data.get("inputs", [])
            for input_data in inputs:
                id = input_data.get("id")
                default_num = json.loads(input_data.get("metadata", {}).get("default", "{}")).get("num")
                self.inputs.append({"id": id, "default_num": default_num})
            else:
                raise ValueError("Invalid message type. Expected 'init'.")
        except Exception as e:
            print(f"Error loading inputs from JSON: {e}")
        print(f"Loaded inputs: {self.inputs}")
    

    def operators(self) -> list:
        """
        Create and return mutation and crossover operators
        """
        mutations = []
        crossovers = []
        mutations.append(Operator("PolynomialMutation", 0.01, 20))
        crossovers.append(Operator("SBXCrossover", 1.0, 20))

        return mutations, crossovers
    
    