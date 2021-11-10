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
    rocchio_clasification(training_collection, test_collection, 0.8, 0.2)

# C:\Users\JOS\Desktop\RecuperacionPRY3\TestFiles\training-set.csv

# C:\Users\JOS\Desktop\RecuperacionPRY3\TestFiles\test-set.csv