import json
from optimization.operator import Operator
from typing import List

class OptimizationData:
    """
    A class used to represent Optimization Data
    """

    def __init__(self, data=None):
        self.population = 10
        self.offspring_population = 1
        self.number_of_objectives = 1
        self.max_evaluations = 200
        self.extra_evaluations = 1
        self.simulation_periods = 1
        self.simulation_iterations = 1
        self.strict_constraint_verification = False
        self.model_id = None
        self.directions = [-1]
        self.inputs = []

        self.lower_bound = []
        self.upper_bound = []
        if data:
            self.load_data(data)
            self.setBounds()

        # Initialize the attributes for the different types of variables
        self.has_int = False
        self.has_float = False
        self.has_binary = False
        self.float_uuid:List[str] = []
        self.float_lower_bound: List[float] = []
        self.float_upper_bound: List[float] = []
        self.int_uuid: List[str] = []
        self.int_lower_bound: List[int] = []
        self.int_upper_bound: List[int] = []
        self.binary_uuid: List[str]= []
        self.number_of_bits: int = None

    def load_data(self, data):
        try:
            self.number_of_constraints = data.get("constraints", 0)

            model = data.get("model", {})
            self.population = model.get("population", 10)
            self.offspring_population = model.get("offspring", 1)
            self.max_evaluations = model.get("maxEvaluations", 200)
            self.extra_evaluations = model.get("extraEvaluations", 0)
            self.strict_constraint_verification = model.get("strictConstraints", False)
            self.simulation_periods = model.get("periods", 1)
            self.simulation_iterations = model.get("iterations", 1)
            self.simulation_model_id = model.get("model_id", None)
            inputs = data.get("inputs", [])
            for input_data in inputs:
                id = input_data.get("id")
                parent = input_data.get("parent")
                try:
                    default_value = json.loads(
                        input_data.get("metadata", {}).get("default", "{}")
                    )
                    if not isinstance(default_value, (int, float, str)):
                        default_value = default_value.get("num")
                        if not isinstance(default_value, (int, float, str)):
                            raise ValueError
                except AttributeError:
                    raise AttributeError(
                        "Invalid message type for default value:" + str(input_data)
                    )
                self.inputs.append({"id": id, "parent": parent, "data": default_value})
            else:
                raise ValueError(
                    "Invalid message type. Expected 'int or float or str'."
                )

        except Exception as e:
            print(f"Error loading inputs from JSON: {e}")
        print(f"Loaded inputs: {self.inputs}")

    def setBounds(self):
        for input in self.inputs:
            if float(input["data"]) > 0:
                self.lower_bound.append(0)
                self.upper_bound.append(1)
            else:
                self.lower_bound.append(-1)
                self.upper_bound.append(0)


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
