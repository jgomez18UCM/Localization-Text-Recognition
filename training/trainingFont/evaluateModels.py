from sklearn.model_selection import KFold
import numpy as np
import os
import shutil
import argparse
import subprocess 

from pathlib import Path
import pathlib

tesstrain_Folder = '/home/tesseract_repos/tesstrain'

#TODO: DUDAS
#Al entrenar el 80% de los datos, con cual? el de texto personalizado o default?

#Hay que borrar el modelo entrenado para que el siguiente este limpio, no?

#El modelo deberia ser uno por cada idioma o uno que soporte todos?

def errorMessage():
    print("\033[31mYou must provide at least lenguage and font name.\033[0m")
    print("\033[36mUsage: python evaluateModels.py -l [lenguaje] -f [fontName]\033[0m")   

def extract_compare_Data(archivos_ordenados, test_index, groundTruthPath, font_Name,lenguage, resultFile):
    
    mainLaunchDir = os.getcwd()

    #Nos movemos al directorio donde se encuentra tesseract
    os.chdir(f'{tesstrain_Folder}')

    last = None
    #Launch tesseract recognition from tesseract folder
    #Al haber 3 archivos con el mismo nombre pero distinta extension, nos guardamos el
    #nombre para omitirlo
    for file in test_index:
        file = archivos_ordenados[file]
        
        #Eliminamos el sufijo ".gt" en caso de que exista
        file_ = Path(file)
        nameFile = file_.name.replace(".gt", "")
        nameFile = pathlib.Path(nameFile).stem

        #omitimos 
        if (last is not None) and (last == nameFile):
            continue
        else:
            print("========================")
            print(nameFile)
            last = nameFile

        #Evaluar, Capturar ambas salidas, escribir y 
        textRecognized = subprocess.run([
                'tesseract',
                f"{groundTruthPath}/{nameFile}.tif",
                'stdout',
                '--tessdata-dir',  
                f'{tesstrain_Folder}/data/{font_Name}_data/{font_Name}-{lenguage}-output',
                '--psm',
                '7',
                '-l',
                f'{font_Name}',
                '--loglevel',
                'ALL',
            ], stdout=subprocess.PIPE)
        
        realText = subprocess.run([
                'cat',
                f"{groundTruthPath}/{nameFile}.gt.txt"
            ],stdout=subprocess.PIPE)
        
        resultFile.write(f"File: {nameFile}\n")
        resultFile.write(f"Real: {realText.stdout.decode()}\n")
        resultFile.write(f"Reco: {textRecognized.stdout.decode()}")
        resultFile.write("Model: Trained with default database.\n")
        resultFile.write("-----------------\n")

    #Volvemos a la carpeta de lanzamiento
    os.chdir(f'{mainLaunchDir}')

def evaluate(lenguage, font_Name):
    groundTruthPath = f'{tesstrain_Folder}/data/{font_Name}_data/{font_Name}-ground-truth/{lenguage}'

    if not os.path.exists(groundTruthPath):
        print(f"WARNING: There is no ground-truth folder for font \"{font_Name}\" and \"{lenguage}\".")
        print(f"Please make sure you generate a ground-truth for \"{font_Name}\" and \"{lenguage}\".")
        return
    
    #Creamos directorio temporal para almacenar los archivos que no se usaran
    mainLaunchDir = os.getcwd()

    temp_folder = mainLaunchDir + "/temp"
    result_folder = mainLaunchDir + "/resultEvaluation"

    if not os.path.exists(temp_folder):
        os.mkdir(temp_folder)

    if not os.path.exists(result_folder):
        os.mkdir(result_folder)

    archivos = os.listdir(groundTruthPath)
    archivos_ordenados = sorted(archivos)
    # print(archivos_ordenados)

    resultFile = open(f"{result_folder}/results.txt", "w")

    kf = KFold(n_splits=5)
    #Entrenamiento y evaluacion
    
    percentage = 0.
    steps = 1.0/5.0
    print(f"\033[33m{round((percentage*100),2)}% of 100%\033[0m")
    for train_index, test_index in kf.split(archivos_ordenados):
        #Mover
        for file in test_index:
            subprocess.run(['mv', '-n',f'{groundTruthPath}/{archivos_ordenados[file]}',  f'{temp_folder}'])

        # archivos = sorted(os.listdir(temp_folder))
        # print(archivos)

        # Entrenar 
        subprocess.run([
            'python',
            'trainTess.py',
            '-l',
            f'{lenguage}',
            '-f',
            f'{font_Name}',
            '-it',
            '400'
            ])

        #Devolver a carpeta
        for file in test_index:
            file = archivos_ordenados[file]
            #Devolver a carpeta
            subprocess.run(['mv', '-n',f'{temp_folder}/{file}', f'{groundTruthPath}'])

        #Extraer datos y esribir en archivo de resultados
        extract_compare_Data(archivos_ordenados, test_index, groundTruthPath, font_Name, lenguage, resultFile)

        #Limpiar modelo (?)
        subprocess.run([
            'python',
            'trainTess.py',
            '-cl',
            '-l',
            f'{lenguage}',
            '-f',
            f'{font_Name}',
            ])

        percentage = percentage + steps
        print(f"\033[33m{round((percentage*100),2)}% of 100%\033[0m")

    #Cerramos fichero
    resultFile.close()

    # # Obtener el primer fold
    # train_index, test_index = next(kf_iter)

    #Eliminamos el directorio temporal
    shutil.rmtree(temp_folder)

def main():
    parser = argparse.ArgumentParser(description='Flags for flags in ground truth.')

    #OPCION PARA CREAR Y LIMPIAR

    parser.add_argument('-l','--lenguage', type=str, help='Lenguage name.', default = None)
    parser.add_argument('-f','--fontname', type=str, help='Font name.', default = None)

    args = parser.parse_args()

    error = 0

    if args.lenguage is not None:
        lenguage = args.lenguage
    else:
        error = 1
    
    if args.fontname is not None:
        font_Name = args.fontname
    else:
        error = 1

    #En caso de que no se defina alguna obligatoria
    if(error == 1):
        errorMessage()
        return    

    evaluate(lenguage, font_Name)
    
    return

if __name__ == "__main__":
    main()