# Imports
import time
from models.Document import Document
from models.Collection import Collection
from models.BayesianClass import BayesianClass
from models.BayesianClassTerm import BayesianClassTerm
import numpy as np


def save_bayesian_results(bayesian_classes, save_path):
    """
    Function that saves the given results of a rocchio classfication in the given path in a txt file
    :type bayesian_classes: dict
    :type save_path: str
    :return None
    """
    timestr = time.strftime("%H-%M-%S")
    try:
        with open(save_path + '\\Bayesian_results (' + timestr + ').txt', 'w') as file:
            file.write(
                f"docid -> clase_real -> clase_asignada_clasificador (similitud)\n\n")
            for doc_id, classification in bayesian_classes.items():
                file.write(
                    f"{str(doc_id)} -> {classification[0]} -> {classification[1]} ({classification[2]})\n")
        file.close()
        print(
            'Un resultado de la clasificación de Bayesianos Ingenuos se ha guardado en \'' + save_path +
            '\\Bayesian_results (' + timestr + ').txt\'')
    except IOError:
        print(
            f"No se pudieron guardar los resultados de la ejecución de Bayesianos Ingenuos")


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
    classified_docs = classify_docs(bayesian_classes, test_coll)
    save_bayesian_results(classified_docs, "..\\Results\\Bayesian")
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
            contribution = (np.log2(p_ip/(1-p_ip))) + \
                (np.log2((1-q_ip)/q_ip))
            bayesian_class.terms[term] = BayesianClassTerm(
                term, p_ip, q_ip, contribution)
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


def classify_docs(bayesian_classes: dict, test_coll: Collection):
    bayesian_classes_result = {}
    for doc_key, document in test_coll.documents.items():
        assigned_class = get_bayesian_class(document, bayesian_classes)
        bayesian_classes_result[doc_key] = [
            str(document.doc_class)] + assigned_class
    return bayesian_classes_result


def get_bayesian_class(document: Document, bayesian_classes):
    highest_sim = ["", 0]
    for class_key, bayesian_class in bayesian_classes.items():
        docxclass_sim = 0
        for term, term_value in document.terms.items():
            if(not term in bayesian_class.terms):
                continue
            docxclass_sim = docxclass_sim + term_value.weight * \
                bayesian_class.terms[term].contribution
            if docxclass_sim > highest_sim[1]:
                highest_sim[0] = bayesian_class.class_name
                highest_sim[1] = docxclass_sim
    return highest_sim
