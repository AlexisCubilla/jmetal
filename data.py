import json

class Data:
    def __init__(self):
        # Initialize the attributes for the different types of variables
        self._has_int = False
        self._has_float = False
        self._has_binary = False
        self._float_uuid = []
        self._float_lower_bound = []
        self._float_upper_bound = []
        self._int_uuid = []
        self._int_lower_bound = []
        self._int_upper_bound = []
        self._binary_uuid = []
        self._number_of_bits = None

        # Initialize the attributes for the optimization functions and parameters
        self.max_evaluations = None
        self.number_of_objectives = None
        self.obj_labels = []
        self.function_uuid=[]
        self.directions = []
        self.population = None
        self.offspring_population = None
        # self.simulation_periods = 0
    
    @property
    def int_uuid(self):
        return self._int_uuid
    @property
    def int_lower_bound(self):
        return self._int_lower_bound
    @property
    def int_upper_bound(self):
        return self._int_upper_bound
    @property
    def float_uuid(self):
        return self._float_uuid
    @property
    def float_lower_bound(self):
        return self._float_lower_bound
    
    @property
    def float_upper_bound(self):
        return self._float_upper_bound
   
    @property
    def binary_uuid(self):
        return self._binary_uuid
    @property
    def number_of_bits(self):
        return self._number_of_bits

    @property
    def has_int(self):
        return self._has_int

    @property
    def has_float(self):
        return self._has_float

    @property
    def has_binary(self):
        return self._has_binary
    
    def add_int_variable(self, uuid, lower, upper):
        self._int_uuid.append(uuid)
        self._int_lower_bound.append(int(lower))
        self._int_upper_bound.append(int(upper))

    def add_float_variable(self, uuid, lower, upper):
        self._float_uuid.append(uuid)
        self._float_lower_bound.append(float(lower))
        self._float_upper_bound.append(float(upper))
       
    def add_binary_variable(self, uuid):
        self._binary_uuid.append(uuid)
        self._number_of_bits += 1
    
    def add_function(self, uuid, direction):
        self.function_uuid.append(uuid)
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
    

    def extract_scenario_data(self, scenario_json) -> None:
        scenario=json.loads(scenario_json)
        variables = scenario["optimization"][0]["optimization_variables"]
        functions = scenario["optimization"][0]["optimization_functions"]

        for var in variables:
            businessObject = var["businessObject"]
            var_type = businessObject["type"]
            lower_bound = businessObject.get("lower_bound")
            upper_bound = businessObject.get("upper_bound")
            uuid = var["variable_id"] if var["variable_id"] else var["variable_n_id"]
            if var_type == "I":
                self.add_int_variable(uuid, lower_bound, upper_bound)
            elif var_type == "F":
                self.add_float_variable(uuid, lower_bound, upper_bound)
            elif var_type == "B":
                self.add_binary_variable(uuid)

            self._has_int = bool(self._int_lower_bound)
            self._has_float = bool(self._float_lower_bound)
            self._has_binary = bool(self._number_of_bits)

        for fn in functions:
            self.add_function(fn["component_id"], fn["direction"])

        businessObject = scenario["optimization"][0]["businessObject"]
        self.number_of_objectives = len(functions)
        self.max_evaluations = int(businessObject["stop_criteria"]["max_evaluations"])
        self.population = int(businessObject["population"])
        self.offspring_population = int(businessObject["offspring_population"])
        # data.simulation_periods = businessObject["simulation_periods"]
        self.print()
   
    # def check_empty_parameters(self):
    #     empty_parameters = []
    #     if not self._has_int and not self._has_float and not self._has_binary:
    #         empty_parameters.append("Variables")
    #     if not self.max_evaluations:
    #         empty_parameters.append("Max evaluations")
    #     if not self.number_of_objectives:
    #         empty_parameters.append("Number of objectives")
    #     if not self.population:
    #         empty_parameters.append("Population")
            
    #     if not self.offspring_population:
    #         empty_parameters.append("Offspring population")

    #     print("Empty data: "+ ", ".join(empty_parameters))
    #     if len(empty_parameters) == 0:
    #         return ""
    #     else:
    #         return "Empty data: "+ ", ".join(empty_parameters)

    def print(self) -> None:
        print(f"has_int: {self._has_int}")
        print(f"has_float: {self._has_float}")
        print(f"has_binary: {self._has_binary}")
        print(f"float_uuid: {self._float_uuid}")
        print(f"float_lower_bound: {self._float_lower_bound}")
        print(f"float_upper_bound: {self._float_upper_bound}")
        print(f"int_uuid: {self._int_uuid}")
        print(f"int_lower_bound: {self._int_lower_bound}")
        print(f"int_upper_bound: {self._int_upper_bound}")
        print(f"binary_uuid: {self._binary_uuid}")
        print(f"number_of_bits: {self._number_of_bits}")
        print(f"max_evaluations: {self.max_evaluations}")
        print(f"number_of_objectives: {self.number_of_objectives}")
        print(f"directions: {self.directions}")
        print(f"population: {self.population}")
        print(f"offspring_population: {self.offspring_population}")

class Operator:
    def __init__(self, name, probability, distribution_index=None):
        self._name = name
        self._probability = probability
        self._distribution_index = distribution_index

    @property
    def name(self):
        return self._name

    @property
    def probability(self):
        return self._probability

    @property
    def distribution_index(self):
        return self._distribution_index
