# Imports
import re
from utils import load_file
from models.term import Term
from models.Document import Document
from models.Collection import Collection

# Constants
TERM_REGEX = r"([a-z0-9\.]+)\/(\d*\.?\d+)"


# Functions
def parse_csv(path):
    """
    Function that parser an entire csv file into a collection object
    :type path:string
    :returns Collection
    """
    file = load_file(path)
    if file is None:
        print("Por favor ingrese una ruta a un archivo válido")
        return None
    file.readline()
    docs = {}
    class_list = []
    class_groups = {}
    term_list = []
    for line in file.readlines():
        fields = line.split("\t")
        terms = parse_terms(term_list, fields[3])
        document = Document(terms, int(fields[0]), fields[2], fields[1])
        docs[str(document.docid)] = document
        insert_doc_group(class_groups, document.doc_class, document.docid)
        insert_class(class_list, document.doc_class)
    collection = Collection(term_list, class_list, class_groups, docs)
    return collection


def parse_terms(term_list, terms):
    """
    :type term_list:list
    :type terms:string
    :returns dict
    """
    term_dict = {}
    parsed_terms = re.findall(TERM_REGEX, terms)
    for raw_term in parsed_terms:
        processed_term = Term(raw_term[0], float(raw_term[1]))
        term_dict[processed_term.term] = processed_term
        insert_term(term_list, processed_term.term)
    return term_dict


def insert_doc_group(class_group: dict, class_name, doc_id):
    """
    :type class_group:dict
    :type class_name:string
    :type doc_id:int
    """
    if class_name in class_group:
        class_group[class_name].append(doc_id)
    else:
        class_group[class_name] = [doc_id]
    return class_group


def insert_class(class_list: list, class_name):
    """
    :type class_list:list
    :type class_name:string
    """
    if not class_name in class_list:
        class_list.append(class_name)
    return class_list


def insert_term(term_list, term):
    """
    :type term_list:list
    :type term:string
    """
    if not term in term_list:
        term_list.append(term)
    return term_list
