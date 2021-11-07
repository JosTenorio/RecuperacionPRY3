
class Term:

    def __init__(self, term, weight):
        """
        :type frequency: int
        :type term: str
        """
        self.term = term
        self.weight = weight
    def __str__(self) -> str:
        return f"Término {self.term}, weight {self.weight}"

