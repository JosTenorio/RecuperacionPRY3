from models.Collection import Collection


def calc_centroids(collection: Collection):
    # pairs of (Beta, gamma)
    params = [(0.75, 0.25), (0.85, 0.15), (0.95, 0.05)]
    rochio_centroids = []
    for param in params:
        for class_name in collection.class_list:
            class_docs = collection.class_groups[class_name]
            non_class_docs = get_complement_docs(
                collection.class_groups, class_name)
            class_vector = calc_class_vector(collection, class_docs, param[0])
            non_class_vector = calc_class_vector(
                collection, non_class_docs, param[1])
            result = subs_vector(class_vector, non_class_vector)
            rochio_centroids.append(result)
    return rochio_centroids


def get_complement_docs(class_groups: dict, class_name):
    classes = []
    for key in class_groups.keys():
        if(key != class_name):
            classes += (class_groups[key])
    return classes


def calc_class_vector(collection: Collection, doc_list, rochio_const):
    cumulative_values = {}
    for doc in doc_list:
        for term in collection.term_list:
            if term in collection.documents[str(doc)].terms:
                value = collection.documents[str(doc)].terms[term]
                add_value(cumulative_values, term, value.weight)
    for key, val in cumulative_values.items():
        cumulative_values[key] = (rochio_const/len(doc_list))*val

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
