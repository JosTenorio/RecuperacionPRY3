class Document:

    def __init__(self, terms: dict, docid: int, num_terms: int, doc_class: str):
        """
        :type num_terms: int
        :type docid: int
        :type doc_class: string
        """
        self.docid = docid
        self.doc_class = doc_class
        self.num_terms = num_terms
        self.terms = terms
        self.training = "a"

    def __str__(self):
        output = (
            f"Documento id {self.docid}, de la clase {self.doc_class}, con {self.num_terms}")
        for term in self.terms:
            output += "\n"+str(term)
        return output
