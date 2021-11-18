# Imports
import numpy as np
from models.Collection import Collection
from models.Document import Document
from utils import get_complement_docs
import time


# Functions
def rocchio_classification(training_coll: Collection, test_coll: Collection, betta, gamma):
    """
    Function that performs rochhio classifacation on the test collection, given the training collection and params
    saves result in a txt file
    :type training_coll: Collection
    :type test_coll:test_coll
    :type betta: float
    :type gamma: float
    :return None
    """
    class_centroids = calc_centroids(training_coll, betta, gamma)
    rocchio_classes = classify_docs(test_coll, class_centroids)
    save_rocchio_results(rocchio_classes, "..\\Results\\Rocchio", betta, gamma)


def save_rocchio_results(rocchio_classes, save_path, betta, gamma):
    """
    Function that saves the given results of a rocchio classfication in the given path in a txt file
    :type rocchio_classes: dict
    :type save_path: str
    :type betta: float
    :type gamma:float
    :return None
    """
    timestr = time.strftime("%H-%M-%S")
    try:
        with open(save_path + '\\Rocchio_results[' + str((betta, gamma)) + '] (' + timestr + ').txt', 'w') as file:
            file.write(
                f"Parametros usados: betta = {str(betta)}, gamma = {str(gamma)}\n")
            file.write(
                f"docid -> clase_real -> clase_asignada_clasificador (similitud)\n\n")
            for doc_id, classification in rocchio_classes.items():
                file.write(
                    f"{str(doc_id)} -> {classification[0]} -> {classification[1]} ({classification[2]})\n")
        file.close()
        print(
            'Un resultado de la clasificación de Rocchio se ha guardado en \'' + save_path + '\\Rocchio_results (' + timestr + ').txt\'')
    except IOError:
        print(f"No se pudieron guardar los resultados de la ejecución de Rocchio con parametros betta = {str(betta)}, "
              f"gamma = {str(gamma)}")


def cacl_sim(doc: Document, centroid_vector):
    """
    Function that calculates de similarity between a given vectorial document and a rocchio centroid
    :type centroid_vector: dict
    :type doc: Document
    :return float
    """
    sim = 0
    for key, value in centroid_vector.items():
        if key in doc.terms:
            sim += value * doc.terms[key].weight
    return sim


def classify_docs(collection: Collection, rocchio_centroids):
    """
    Given a test collection and a dictionary of class centroids, this functions classifies the documents with the
    rocchio method
    :type collection: Collection
    :type rocchio_centroids: dict
    :return dict
    """
    rocchio_classes = {}
    for doc_id, doc in collection.documents.items():
        rocchio_classes[doc_id] = [doc.doc_class] + \
                                  get_rocchio_class_rank(doc, rocchio_centroids)
    return rocchio_classes


def get_rocchio_class_rank(doc: Document, rocchio_centroids):
    """
    Classifies the given document into one of the classes given via the rocchio calculated centroids
    rocchio method
    :type doc: Document
    :type rocchio_centroids: dict
    :return list
    """
    class_rank = []
    for class_name, centroid in rocchio_centroids.items():
        sim = cacl_sim(doc, centroid)
        class_rank.append([class_name, sim])
    class_rank.sort(key=lambda x: x[1])
    return class_rank


def calc_centroids(collection: Collection, betta, gamma):
    """
    Calculates class centroids based on the rochio metod.
    :type collection: Collection
    :type betta: float
    :type gamma: float
    returns rochio_centroids: Dict
    """
    rocchio_centroids = {}
    for class_name in collection.class_list:
        class_docs = collection.class_groups[class_name]
        non_class_docs = get_complement_docs(
            collection.class_groups, class_name)
        class_vector = calc_class_vector(collection, class_docs, betta)
        non_class_vector = calc_class_vector(collection, non_class_docs, gamma)
        # class_vector = normalize_centroid(class_vector)
        # non_class_vector = normalize_centroid(non_class_vector)
        centroid = subs_vector(class_vector, non_class_vector)
        centroid = normalize_centroid(centroid)
        rocchio_centroids[class_name] = centroid
    return rocchio_centroids


def normalize_centroid(centroid):
    """
    Returns the normalized centroid of the given centroid vector
    :type centroid: dict
    :return dict
    """
    vector_norm = np.linalg.norm(list(centroid.values()))
    normalized_list_dict = [(k, (v / vector_norm).item())
                            for k, v in centroid.items()]
    return dict(normalized_list_dict)


def calc_class_vector(collection: Collection, doc_list, rocchio_const):
    cumulative_values = {}
    for doc in doc_list:
        for term in collection.term_list:
            if term in collection.documents[str(doc)].terms:
                value = collection.documents[str(doc)].terms[term]
                add_value(cumulative_values, term, value.weight)
    for key, val in cumulative_values.items():
        cumulative_values[key] = (rocchio_const / len(doc_list)) * val
    return cumulative_values


def add_value(cumulative_values, term, value):
    """
    type:term_list(list)
    type:term(string)
    """
    if term in cumulative_values:
        cumulative_values[term] += value
    else:
        cumulative_values[term] = value
    return cumulative_values


def subs_vector(class_vector, non_class_vector):
    for key, value in non_class_vector.items():
        if key in class_vector:
            class_vector[key] -= value
        else:
            class_vector[key] = -value
    return class_vector
