from utils import load_file
from models.term import Term
from models.Document import Document
import re
# Global variable
regex = r"([a-z0-9\.]+)\/(\d*\.?\d+)"

"""
    Function that returns a dictionary of terms given a csv file with the next format:
    [documentId]\t[class]\t[termCount]\t[term/termWeight\s+]+
    :type path: string
"""
def parse_csv(path):
    file=load_file(path)
    if(file==None):
        print("Por favor ingrese una ruta a un archivo válido")
        return None
    file.readline()
    docs={}
    for line in file.readlines():
        fields = line.split("\t")
        terms = parseTerms(fields[3])
        document = Document(terms,fields[0],fields[2],fields[1])
        docs[str(document.docid)]=document
    return docs
def parseTerms(terms):
    term_list=[]
    parsedTerms=re.findall(regex,terms)
    for raw_term in parsedTerms:
        processed_term = Term(raw_term[0],raw_term[1])
        term_list.append(processed_term)
    return term_list
