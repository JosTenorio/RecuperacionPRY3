from controllers.parse_controller import parse_csv
from controllers.rochio_controller import rocchio_clasification

"""
Main program execution
"""
if __name__ == '__main__':
    training_path = input("Ingrese la ruta de la colección de entrenamiento\n>>")
    test_path = input("Ingrese la ruta de la colección de prueba\n>>")
    training_collection = parse_csv(training_path)
    test_collection = parse_csv(test_path)
    rocchio_clasification(training_collection, test_collection, 0.75, 0.25)
    rocchio_clasification(training_collection, test_collection, 0.85, 0.15)
    rocchio_clasification(training_collection, test_collection, 0.95, 0.05)
