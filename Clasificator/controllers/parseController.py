from utils import load_file
from models.term import Term
from models.Document import Document
from models.Collection import Collection
import re
# Global variable
regex = r"([a-z0-9\.]+)\/(\d*\.?\d+)"

"""
    Function that returns a dictionary of terms given a csv file with the next format:
    [documentId]\t[class]\t[termCount]\t[term/termWeight\s+]+
    :type path: string
"""


def parse_csv(path):
    file = load_file(path)
    if(file == None):
        print("Por favor ingrese una ruta a un archivo válido")
        return None
    file.readline()
    docs = {}
    class_list = []
    term_list = []
    class_groups = {}
    for line in file.readlines():
        fields = line.split("\t")
        terms = parseTerms(term_list, fields[3])
        document = Document(terms, int(fields[0]), fields[2], fields[1])
        docs[str(document.docid)] = document
        insert_doc_group(class_groups, document.doc_class, document.docid)
        insert_class(class_list, document.doc_class)
    collection = Collection(term_list, class_list, class_groups, docs)
    return collection


def parseTerms(term_list: list, terms):

    term_dict = {}
    parsedTerms = re.findall(regex, terms)
    for raw_term in parsedTerms:
        processed_term = Term(raw_term[0], raw_term[1])
        term_dict[processed_term.term] = processed_term
        insert_term(term_list, processed_term.term)
    return term_dict


def insert_doc_group(class_group: dict, class_name, docid):
    if class_name in class_group:
        class_group[class_name].append(docid)
    else:
        class_group[class_name] = [docid]
    return class_group


def insert_class(class_list: list, class_name):
    if not class_name in class_list:
        class_list.append(class_name)
    return class_list


def insert_term(term_list, term):
    if not term in term_list:
        term_list.append(term)
    return term_list
