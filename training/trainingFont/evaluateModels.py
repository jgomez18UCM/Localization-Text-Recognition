from sklearn.model_selection import KFold
import numpy as np
import os
import shutil
import argparse
import subprocess 

from pathlib import Path
import pathlib

tesstrain_Folder = '/home/tesseract_repos/tesstrain'

#Hay que borrar el modelo entrenado para que el siguiente este limpio, no?
#El modelo deberia ser uno por cada idioma o uno que soporte todos?
#Hay que lanzar el modelo para cada 

def errorMessage():
    print("ERROR!")
    print("You must provide at least lenguage and font name.")
    print("Usage: python evaluateModels.py -l [lenguaje] -f [fontName]")   

def extract_compare_Data(archivos_ordenados, test_index, groundTruthPath, font_Name,lenguage, result_folder):
    
    resultFile = open(f"{result_folder}/results.txt", "w")
    
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

    resultFile.close()

def evaluate(lenguage, font_Name):
    groundTruthPath = f'{tesstrain_Folder}/data/{font_Name}_data/{font_Name}-ground-truth/{lenguage}'

    if not os.path.exists(groundTruthPath):
        print(f"There is no ground truth folder for font {font_Name} and {lenguage}")
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

    kf = KFold(n_splits=5)
    #Entrenamiento y evaluacion

    primeraVez = False
    
    for train_index, test_index in kf.split(archivos_ordenados):

        if primeraVez == True:
            break
        else: 
            primeraVez = True 

        # for i in test_index:
            # print(archivos_ordenados[i])

        #Mover
        for file in test_index:
            subprocess.run(['mv', '-n',f'{groundTruthPath}/{archivos_ordenados[file]}',  f'{temp_folder}'])

        # archivos = os.listdir(temp_folder)
        # archivos_ordenados = sorted(archivos)
        # print(archivos_ordenados)

        #Entrenar 

        #Devolver a carpeta
        for file in test_index:
            file = archivos_ordenados[file]
            #Devolver a carpeta
            subprocess.run(['mv', '-n',f'{temp_folder}/{file}', f'{groundTruthPath}'])

        #Extraer datos y esribir en archivo de resultados
        extract_compare_Data(archivos_ordenados, test_index, groundTruthPath, font_Name, lenguage, result_folder)

        #Limpiar modelo (?)

        os.chdir(f'{mainLaunchDir}')


    # # Obtener el primer fold
    # train_index, test_index = next(kf_iter)

    # # print("Train: ", train_index)
    # # print("Test: ", test_index)
    # print("Train Size ", len(train_index))
    # print("Test Size ", len(test_index))
    # for i in test_index:
    #     print(archivos_ordenados[i])

    #falta moverlas,que entrene, evaluar cada una, escribir su resultado y 
    # exdevovler las sacadas, sacar y entrenar ...

    # for train_index, test_index in kf.split(archivos_ordenados):
    # print("Índices de entrenamiento:", train_index, "Índices de prueba:", test_index)
    # X_train, X_test = X[train_index], X[test_index]
    # y_train, y_test = y[train_index], y[test_index]

    # print("Datos de entrenamiento:")
    # print("X:", X_train)
    # print("Y:", y_train)

    # print("Datos de prueba:")
    # print("X:", X_test)
    # print("Y:", y_test)

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