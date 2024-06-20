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