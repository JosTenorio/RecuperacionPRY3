# Imports
import re

# Constants
regex_paths = r'[A-z]:\\(?:[^\\\/:*?"<>|\r\n]+\\)*[^\\\/:*?"<>|\r\n]*'
regex_files = r'[a-zA-Z]:[\\\/](?:[a-zA-Z0-9\_-]+[\\\/])*([a-zA-Z0-9\_\-]+\.csv)'


# Functions
def is_path(path):
    return bool(re.match(regex_paths, path))


def is_file(path):
    return bool(re.match(regex_files, path))


def open_file(path):
    try:
        file = open(path)
        return file
    except UnicodeDecodeError:
        print(
            "Los archivos deben estar en formato utf-8, se seguirá la ejecución pero puede que los resultados se vean "
            "afectados")
        file = open(path)
        return file
    except FileNotFoundError:
        raise FileNotFoundError("No se encontró el archivo")


def load_file(path):
    if not is_file(path):
        return None
    return open_file(path)


def get_complement_docs(class_groups: dict, class_name):
    classes = []
    for key in class_groups.keys():
        if key != class_name:
            classes += (class_groups[key])
    return classes
