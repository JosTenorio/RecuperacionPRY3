class Collection:
    def __init__(self, term_list, class_list, class_groups, documents):
        """
        :type num_terms: int
        :type docid: int
        :type doc_class: string
        """
        self.term_list = term_list
        self.class_list = class_list
        self.class_groups = class_groups
        self.documents = documents
