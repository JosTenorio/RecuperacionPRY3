class BayesianClassTerm:
    def __init__(self, term, p_ip, q_ip, contribution):
        """
        :type term: str
        :type p_ip: float
        :type q_ip: float
        """
        self.term = term
        self.p_ip = p_ip
        self.q_ip = q_ip
        self.contribution = contribution

    def __str__(self) -> str:
        return f"Término {self.term}, Pip = {self.p_ip} Qip = {self.q_ip} Contribution = {self.contribution}"
