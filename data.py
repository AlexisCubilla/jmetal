class Data:
    def __init__(self):
        self.has_int = False
        self.has_float = False
        self.has_binary = False
        self.float_lower_bound = []
        self.float_upper_bound = []
        self.int_lower_bound = []
        self.int_upper_bound = []
        self.number_of_bits = 0
        self.max_evaluations = 0
        self.max_seconds = 0
        self.number_of_objectives = 0
        self.directions = []
        self.population = 0
        self.offspring_population = 0
        self.simulation_periods = 0
     
    def operators(self) -> list:
        mutations = []
        crossovers = []
        if self.has_float:
            mutations.append(Operator("PolynomialMutation", 0.01, 20))
            crossovers.append(Operator("SBXCrossover", 1.0, 20))
        if self.has_int:
            mutations.append(Operator("IntegerPolynomialMutation", 0.01, 20))
            crossovers.append(Operator("IntegerSBXCrossover", 1.0, 20))
        if self.has_binary:
            mutations.append(Operator("BitFlipMutation", 0.01))
            crossovers.append(Operator("SPXCrossover", 1.0))

        return mutations, crossovers
    

    
    

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
    