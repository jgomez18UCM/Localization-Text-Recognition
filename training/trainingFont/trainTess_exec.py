import subprocess
import argparse 

import time
import datetime

from trainClasses.TrainOCR import TrainOCR
from trainClasses.Constants import *

def errorMessage():
    print("\033[31mYou must provide at least lenguage, font name and a number of iterations.\033[0m")
    print("\033[36mUsage: python trainTess_exec.py -l [lenguaje] -f [fontName] -it [natural number]\033[0m")    

def main():
    parser = argparse.ArgumentParser(description='Flags for flags in ground truth.')

    #OPCION PARA CREAR Y LIMPIAR

    parser.add_argument('-l','--lenguage', type=str, help='Lenguage name.', default = None)
    parser.add_argument('-f','--fontname', type=str, help='Font name.', default = None)
    parser.add_argument('-it','--iterations', type=str, help='Max training iterations.', default = None)
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

    #Crear la instancia
    trainerInstance = TrainOCR()

    #En caso de que se especifique limpiar
    if (args.clear is not False) and error != 1:
        trainerInstance.clear(language, font_Name)
        # clear(lenguage, font_Name)
        return
    elif error == 1:
        errorMessage()
        return

    if args.iterations is not None:
        maxIterations = args.iterations
    else:
        error = 1

    #En caso de que no se defina alguna obligatoria
    if(error == 1):
        errorMessage()
        return

    #Mover de tessdata_best a /home/tetesseract_repos/langdata los trainneddata
    subprocess.run(['cp', '-n',f'{tessdata_best_Folder}/{language}.traineddata',  f'{tesseract_Folder}/tessdata'])
    
    start_time = time.time()

    trainerInstance.train(language, font_Name, maxIterations)
    # trainOCR(language, font_Name, maxIterations)

    end_time = time.time()
    elapsed_time = end_time - start_time

    # Creamos un objeto datetime a partir de la diferencia de tiempo
    delta_time = datetime.datetime.utcfromtimestamp(elapsed_time)

    # Formateamos el objeto datetime en minutos, segundos y milisegundos utilizando strftime
    print("Tiempo transcurrido: {}".format(delta_time.strftime('%H:%M:%S.%f')))

if __name__ == "__main__":
    main()