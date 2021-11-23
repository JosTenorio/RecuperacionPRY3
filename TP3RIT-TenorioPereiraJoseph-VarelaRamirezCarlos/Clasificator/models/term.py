
class Term:

    def __init__(self, term, weight):
        """
        :type weight: float
        :type term: str
        """
        self.term = term
        self.weight = weight

    def __str__(self) -> str:
        return f"Término {self.term}, peso {self.weight}"
