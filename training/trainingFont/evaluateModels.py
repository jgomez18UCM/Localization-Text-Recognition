from sklearn.model_selection import KFold
import numpy as np
import os
import shutil
import argparse
import subprocess 
import json

from pathlib import Path
import pathlib

langdata_lstm_Folder = '/home/tesseract_repos/langdata_lstm'
tesstrain_Folder = '/home/tesseract_repos/tesstrain'

def extract_compare_Data(archivos_ordenados, test_index, groundTruthPath, font_Name,lenguage, resultFile, modelUsed):
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
            print(f'\033[36mRecognizing {nameFile}.\033[0m')
            last = nameFile

        #Evaluar, Capturar ambas salidas, escribir y 
        textRecognized = subprocess.run([
                'tesseract',
                f"{groundTruthPath}/{nameFile}.tif",
                'stdout',
                '--tessdata-dir',  
                f'{tesstrain_Folder}/data/{font_Name}_data/{font_Name}-{lenguage}-output',
                '--user-words',
                f'{langdata_lstm_Folder}/{lenguage}',
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
        

        file = {}
        file.update({
            "Model": f"{modelUsed}",
            "Real": f"{realText.stdout.decode()}",
            "Reco": f"{textRecognized.stdout.decode()}",
        })


        resultFile.update({
            f"{nameFile}": file,
        })

    #Volvemos a la carpeta de lanzamiento
    os.chdir(f'{mainLaunchDir}')

def clearModel(lenguage, font_Name):
    subprocess.run([
            'python',
            'trainTess.py',
            '-cl',
            '-l',
            f'{lenguage}',
            '-f',
            f'{font_Name}',
            ])

def modelEvaluation(kf,archivos_ordenados, groundTruthPath, temp_folder, lenguage, font_Name, resultFile, trainCommand, modelName):
    percentage = 0.
    steps = 1.0/5.0
    for train_index, test_index in kf.split(archivos_ordenados):
        # if firstTime == False:
        #     firstTime = True
        # else: 
        #     return
        #Mover
        for file in test_index:
            subprocess.run(['mv', '-n',f'{groundTruthPath}/{archivos_ordenados[file]}',  f'{temp_folder}'])

        # archivos = sorted(os.listdir(temp_folder))
        # print(archivos)

        # Entrenar 
        trainCommand()

        # #Devolver a carpeta
        for file in test_index:
            file = archivos_ordenados[file]
            #Devolver a carpeta
            subprocess.run(['mv', '-n',f'{temp_folder}/{file}', f'{groundTruthPath}'])

        #Extraer datos y esribir en archivo de resultados
        extract_compare_Data(archivos_ordenados, test_index, groundTruthPath, font_Name, lenguage, resultFile, modelName)

        #Limpiar modelo 
        clearModel(lenguage, font_Name)

        percentage = percentage + steps
        print(f"\033[33mEvaluation:{round((percentage*100),2)}% of 100%\033[0m")

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

    #Generamos particion de 5 grupos para la evaluación.
    kf = KFold(n_splits=5)
    
    #Entrenamiento y evaluacion
    #Modelos
    #=====================================  A: Default Tesseract
    resultFile = {}
    #Este solo va a ejecutar no? sin entrenar. solo probar.
    modelEvaluation(kf, archivos_ordenados, groundTruthPath, temp_folder, lenguage, font_Name, resultFile,
                     lambda: None,
                    "Base tesseract model")
    #Escribimos en  fichero y cerramos
    with open(f"{result_folder}/resultsModel_Default_A.json", "w") as archivo_json:
        json.dump(resultFile, archivo_json, indent = 4)
    
    #=====================================  B: Trained Font overfitted
    #Limpiamos el ground truth que haya
    subprocess.run([ 'python', 'groundTruth.py', '-cl', '-l',f'{lenguage}','-f',f'{font_Name}'])
    #Creamos el ground truth
    subprocess.run([ 'python', 'groundTruth.py','-l',f'{lenguage}','-f',f'{font_Name}'])
    resultFile = {}

    modelEvaluation(kf, archivos_ordenados, groundTruthPath, temp_folder, lenguage, font_Name, resultFile,
                     lambda: subprocess.run([
                            'python',
                            'trainTess.py',
                            '-l',
                            f'{lenguage}',
                            '-f',
                            f'{font_Name}',
                            '-it',
                            '100'
                            ]),
                    f"Train a model with a special font: {font_Name}")
    
    with open(f"{result_folder}/resultsModel_Font_B.json", "w") as archivo_json:
        json.dump(resultFile, archivo_json, indent = 4)
    
    # ===================================== C: Trained Font overfitted to custom grount truth test
    #Limpiamos el ground truth que haya
    subprocess.run([ 'python', 'groundTruth.py', '-cl', '-l',f'{lenguage}','-f',f'{font_Name}'])
    #Creamos ground truth con texto personalizado
    customTextPath= "/home/trainingFont/dialogos/"
    subprocess.run([ 'python', 'groundTruth.py', '-l',f'{lenguage}','-f',f'{font_Name}', '-dir' , customTextPath])
    
    resultFile = {}
    modelEvaluation(kf, archivos_ordenados, groundTruthPath, temp_folder, lenguage, font_Name, resultFile)
    modelEvaluation(kf, archivos_ordenados, groundTruthPath, temp_folder, lenguage, font_Name, resultFile,
                     lambda: subprocess.run([
                            'python',
                            'trainTess.py',
                            '-l',
                            f'{lenguage}',
                            '-f',
                            f'{font_Name}',
                            '-it',
                            '100'
                            ]),
                    f"Train a model with a special font: {font_Name} and text:{customTextPath}")


    #Escribimos en fichero y cerramos
    with open(f"{result_folder}/resultsModel_Custom_C.json", "w") as archivo_json:
        json.dump(resultFile, archivo_json, indent = 4)
        
    #=====================================  Eliminamos el directorio temporal
    shutil.rmtree(temp_folder)

def main():
    parser = argparse.ArgumentParser(description='Flags for evaluate models.')
    parser.add_argument('-l','--lenguage', type=str, help='Lenguage name.', default = None)
    parser.add_argument('-f','--fontname', type=str, help='Font name.', default = None)

    #Tres posibles modelos
    #A: modelo base de tesseract
    #B: modelo entrenado con una fuente especial
    #C: modelo entrenado con una fuente especial y con un texto especial
    parser.add_argument('-A','--A', action='store_true', help='Base tesseract model.')
    parser.add_argument('-B','--B', action='store_true', help='Train a model with a special font.')
    parser.add_argument('-C','--C', action='store_true', help='Train a model with a special font and text.')

    args = parser.parse_args()

    if args.lenguage is not None:
        lenguage = args.lenguage
    else:
        print("\033[31mYou must provide at least lenguage to train any model.\033[0m")
        print("\033[36mUsage: python evaluateModels.py -l [lenguaje] -A\033[0m") 
        return
    
    #Si no se especifia alguno, se entrenan todos
    trainAll = not(args.A or args.B or args.C)

    #Solo se verifica en los modelos B y C, antes de entrenar para lanzar error
    if ((args.B is True or args.C is True) or trainAll):
        if args.fontname is not None:
            font_Name = args.fontname
        else:
            print("\033[31mYou must provide at least lenguage and font name to train models B or C.\033[0m")
            print("\033[36mUsage: python evaluateModels.py -l [lenguaje] -f [fontName] -B -C \033[0m") 
            return

    if args.A is True:
        #Entrenar y evaluar modelo A
        print("Training A")
        n = 0
    
    #En caso de que si se haya definido fontName
    if args.fontname is not None:
        if args.B is True:
                #Entrenar y evaluar modelo B
                print("Training B")
                n = 0

        if args.C is True:
            print("Training C")
            #Entrenar y evaluar modelo C
            n = 0

    # evaluate(lenguage, font_Name)
    
    if trainAll:
        print("Training all")
    return

if __name__ == "__main__":
    main()