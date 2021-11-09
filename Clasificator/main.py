from controllers.parse_controller import parse_csv
from controllers.rochio_controller import calc_centroids

"""
Main program execution
"""
if __name__ == '__main__':
    print("Ingrese la ruta\n>>")
    path = input()
    collection = parse_csv(path)

    calc_centroids(collection)
