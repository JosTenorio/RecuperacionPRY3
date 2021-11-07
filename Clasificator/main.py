from utils import is_file
from controllers.parseController import parse_csv



if __name__ == '__main__':
    print("Ingrese la ruta\n>>")
    path=input()
    data = parse_csv(path)
    for da in data:
        print(data[da])
    print('PyCharm')

