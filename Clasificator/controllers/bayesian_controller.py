# Imports
from models.Collection import Collection
from models.BayesianClass import BayesianClass
from models.BayesianClassTerm import BayesianClassTerm


# Functions
def bayesian_classification(training_coll: Collection, test_coll: Collection):
    """
    Function that performs ingenious bayesian classification on the test collection, given the training collection and
    saves result in a txt file
    :type training_coll: Collection
    :type test_coll:test_coll
    :return None
    """
    bayesian_classes = calc_bysn_classes(training_coll)
    # bayesian_classes = {class_name : BayesianClass}
    return


def calc_bysn_classes(collection: Collection):
    """
    Function that, given a collection, calculates the p_ip and q_ip of every combination of class and term found in
    the given collection
    :type collection: Collection
    :return dict
    """
    bayesian_classes = {}
    N_t = len(collection.documents.items())
    for class_name in collection.class_list:
        class_docs = collection.class_groups[class_name]
        n_p = len(class_docs)
        bayesian_class = BayesianClass(class_name)
        for term in collection.term_list:
            n_ip, n_i = calc_term_stats(collection, term, class_docs)
            p_ip = (1 + n_ip) / (2 + n_p)
            q_ip = (1 + (n_i - n_ip)) / (2 + (N_t - n_p))
            bayesian_class.terms[term] = BayesianClassTerm(term, p_ip, q_ip)
        bayesian_classes[class_name] = bayesian_class
    return bayesian_classes


def calc_term_stats(collection: Collection, term, class_docs):
    """
    Function that, given a term and the docs in a class, calculates the amount of docs that have the term (n_1) and
    the amount of docs in the class that have the term (n_ip)
    :type collection: Collection
    :type term: str
    :type class_docs: list
    :return list
    """
    n_ip = 0
    n_i = 0
    for doc_id, doc in collection.documents.items():
        if term in doc.terms.keys():
            n_i += 1
            if int(doc_id) in class_docs:
                n_ip += 1
    return [n_ip, n_i]
