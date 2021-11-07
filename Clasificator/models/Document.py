class Document:

    def __init__(self,terms,docid,num_terms,doc_class):
        """
        :type num_terms: int
        :type docid: int
        :type doc_class: string
        """
        self.docid = docid
        self.doc_class = doc_class
        self.num_terms = num_terms
        self.terms = terms
        
    def __str__(self):
        output=(f"Documento id {self.docid}, de la clase {self.doc_class}, con {self.num_terms}")
        for term in self.terms:
            output+="\n"+str(term)
        return output