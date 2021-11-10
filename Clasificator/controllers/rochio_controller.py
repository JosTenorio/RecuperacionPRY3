from models.Collection import Collection
from models.Document import Document
import time


def rocchio_clasification(training_coll: Collection, test_coll: Collection, betta, gamma):
    class_centroids = calc_centroids(training_coll, betta, gamma)
    rocchio_classes = classify_docs(test_coll, class_centroids)
    save_rocchio_results(rocchio_classes, "..\\Results", betta, gamma)


def save_rocchio_results(rocchio_classes, save_path, betta, gamma):
    timestr = time.strftime("%H-%M-%S")
    try:
        with open(save_path + '\\Rocchio_results (' + timestr + ').txt', 'w') as file:
            file.write(f"Parametros usados: betta = {str(betta)}, gamma = {str(gamma)}\n")
            file.write(f"docid -> clase_real -> clase_asignada_clasificador (similitud)\n\n")
            for doc_id, classification in rocchio_classes.items():
                file.write(f"{str(doc_id)} -> {classification[0]} -> {classification[1]} ({classification[2]})\n")
        file.close()
    except IOError:
        print(f"No se pudieron guardar los resultados de la ejecución de Rocchio con parametros betta = {str(betta)}, "
              f"gamma = {str(gamma)}")
    return


def cacl_sim(doc: Document, centroid_vector):
    sim = 0
    for key, value in centroid_vector.items():
        if key in doc.terms:
            sim += value * doc.terms[key].weight
    return sim


def classify_docs(collection: Collection, rocchio_centroids):
    rocchio_classes = {}
    for doc_id, doc in collection.documents.items():
        rocchio_classes[doc_id] = [doc.doc_class] + get_rocchio_class(doc, rocchio_centroids)
    return rocchio_classes


def get_rocchio_class(doc: Document, rocchio_centroids):
    highest_sim = ["", 0]
    first = True
    for class_name, centroid in rocchio_centroids.items():
        sim = cacl_sim(doc, centroid)
        if first:
            highest_sim[1] = sim
            highest_sim[0] = class_name
            first = False
        elif highest_sim[1] < sim:
            highest_sim[0] = class_name
            highest_sim[1] = sim
        else:
            pass
    return highest_sim


def calc_centroids(collection: Collection, betta, gamma):
    rocchio_centroids = {}
    for class_name in collection.class_list:
        class_docs = collection.class_groups[class_name]
        non_class_docs = get_complement_docs(collection.class_groups, class_name)
        class_vector = calc_class_vector(collection, class_docs, betta)
        non_class_vector = calc_class_vector(collection, non_class_docs, gamma)
        result = subs_vector(class_vector, non_class_vector)
        rocchio_centroids[class_name] = result
    return rocchio_centroids


def get_complement_docs(class_groups: dict, class_name):
    classes = []
    for key in class_groups.keys():
        if key != class_name:
            classes += (class_groups[key])
    return classes


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
    # print(f"termino {value}")

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
