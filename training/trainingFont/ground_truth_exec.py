import argparse

from trainClasses.GroundTruth import GroundTruth
from trainClasses.Constants import *

def main():
    parser = argparse.ArgumentParser(description='Flags for flags in ground truth.')

    parser.add_argument('-dir','--directory', type=str, help='Directory path with training text.', default = None)
    parser.add_argument('-l','--lenguage', type=str, help='Lenguage name.', default = None)
    parser.add_argument('-f','--fontname', type=str, help='Font name.', default = None)
    parser.add_argument('-cl','--clear', action='store_true', help='Clear ground truth folder.')

    args = parser.parse_args()

    error = 0
    #Si no se define una flag obligatoria salta error.
    if args.lenguage is not None:
        language = args.lenguage
    else:
        error = 1
    
    if args.fontname is not None:
        font_Name = args.fontname
    else:
        error = 1

    #En caso de que no se defina alguna obligatoria
    if(error == 1):
        print("\033[31mYou must provide at least lenguage and font name.\033[0m")
        print("\033[36Usage: python ground_truth_exec.py -l [lenguaje] -f [fontName]\033[0m")
        return 

    #Ruta por defecto
    path = f'{langdata_lstm_Folder}/{language}'

    #Ruta personalizada
    if args.directory is not None:
        path = args.directory 

    groundTruthInstance = GroundTruth(path)

    #En caso de que se especifique limpiar
    if args.clear is True:
        groundTruthInstance.clear(language, font_Name)
        return

    groundTruthInstance.create(language, font_Name)

if __name__ == "__main__":
    main()