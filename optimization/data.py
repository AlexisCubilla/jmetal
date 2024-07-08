import json

from optimization.operator import Operator

class OptimizationData:
    def __init__(self, data=None):
        # Initialize the attributes for the different types of variables
        self.has_int = False
        self.has_float = False
        self.has_binary = False
        self.float_uuid = []
        self.float_lower_bound = []
        self.float_upper_bound = []
        self.int_uuid = []
        self.int_lower_bound = []
        self.int_upper_bound = []
        self.binary_uuid = []
        self.number_of_bits = 0

        # Initialize the attributes for the optimization functions and parameters
        self.max_evaluations = None
        self.extra_evaluations = None
        self.number_of_objectives = None
        self.obj_labels = []
        self.objective_uuid=[]
        self.directions = []
        self.population = None
        self.offspring_population = None
        self.periods = None
        self.iterations = None

        if data:
            self.load_data(data)
            
    def add_int_variable(self, uuid, lower, upper):
        self.int_uuid.append(uuid)
        self.int_lower_bound.append(int(lower))
        self.int_upper_bound.append(int(upper))

    def add_float_variable(self, uuid, lower, upper):
        self.float_uuid.append(uuid)
        self.float_lower_bound.append(float(lower))
        self.float_upper_bound.append(float(upper))
       
    def add_binary_variable(self, uuid):
        self.binary_uuid.append(uuid)
        self.number_of_bits += 1
    
    def add_objective(self, uuid, direction):
        self.objective_uuid.append(uuid)
        self.directions.append(direction)
    
    def operators(self) -> list:
        mutations = []
        crossovers = []

        if self.has_int:
            mutations.append(Operator("IntegerPolynomialMutation", 0.01, 20))
            crossovers.append(Operator("IntegerSBXCrossover", 1.0, 20))
        if self.has_float:
            mutations.append(Operator("PolynomialMutation", 0.01, 20))
            crossovers.append(Operator("SBXCrossover", 1.0, 20))

        if self.has_binary:
            mutations.append(Operator("BitFlipMutation", 0.01))
            crossovers.append(Operator("SPXCrossover", 1.0))

        return mutations, crossovers
    

    def load_data(self, received_data: dict) -> None:
        attrs = ["max_evaluations", "extra_evaluations", "population", "offspring_population",
                 "number_of_objectives", "periods", "iterations", "outputs", "periods", "iterations"]
        for attr in attrs:
            setattr(self, attr, received_data.get(attr, None))

        variable_addition = {
            "integer": self.add_int_variable,
            "float": self.add_float_variable,
            "binary": self.add_binary_variable
        }
        
        for input in received_data.get("inputs", []):
            add_variable_func = variable_addition.get(input["type"])
            if add_variable_func:
                if input["type"] == "binary":
                    add_variable_func(input["id"])
                else:
                    add_variable_func(input["id"], input["lowerBound"], input["upperBound"])

        self.has_binary = bool(self.number_of_bits)
        self.has_int = bool(self.int_uuid)
        self.has_float = bool(self.float_uuid)
        
        for output in received_data.get("outputs", []):
            self.add_objective(output["id"], 1 if output["objective"] == "maximize" else -1)
        self.print()    
          
    def print(self) -> None:
        print(f"has_int: {self.has_int}")
        print(f"has_float: {self.has_float}")
        print(f"has_binary: {self.has_binary}")
        print(f"float_uuid: {self.float_uuid}")
        print(f"float_lower_bound: {self.float_lower_bound}")
        print(f"float_upper_bound: {self.float_upper_bound}")
        print(f"int_uuid: {self.int_uuid}")
        print(f"int_lower_bound: {self.int_lower_bound}")
        print(f"int_upper_bound: {self.int_upper_bound}")
        print(f"binary_uuid: {self.binary_uuid}")
        print(f"number_of_bits: {self.number_of_bits}")
        print(f"max_evaluations: {self.max_evaluations}")
        print(f"number_of_objectives: {self.number_of_objectives}")
        print(f"objective_uuid: {self.objective_uuid}")
        print(f"directions: {self.directions}")
        print(f"population: {self.population}")
        print(f"offspring_population: {self.offspring_population}")
        print(f"periods: {self.periods}")
        print(f"iterations: {self.iterations}")
