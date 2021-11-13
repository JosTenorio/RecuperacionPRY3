class BayesianClass:
    def __init__(self, class_name):
        """
        :type Pip: float
        :type Pip: float
        :type Qip: float
        """
        self.class_name = class_name
        self.terms = {}

    def __str__(self) -> str:
        output = (
            f"Clase: {self.class_name}, con los términos")
        for term in self.terms.values():
            output += "\n"+str(term)
        return output

