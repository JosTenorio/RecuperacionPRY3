from controllers.parseController import parse_csv


terminos = ["terminos"]
if __name__ == '__main__':
    print("Ingrese la ruta\n>>")
    path = input()
    collection = parse_csv(path)
    for class_name in collection.class_list:
        print(class_name)
    # for term in collection.term_list:
    #     print(term)
    for key in collection.class_groups:
        print(collection.class_groups[key])
