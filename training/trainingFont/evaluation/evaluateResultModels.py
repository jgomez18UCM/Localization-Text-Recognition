import argparse
import json
import difflib
import os


def errorMessage():
    print("\033[31mYou must provide models results json full folder path .\033[0m")
    print("\033[36mUsage: python evaluateResultsModels.py -folder [folderPath]\033[0m")

def evaluateFolderResults(folderPath):
    folder = os.listdir(folderPath)
    for file in folder:
        filePath = None
        if(not folderPath.endswith("/")):
            filePath = folderPath +"/"+ file
        else:
            filePath = folderPath + file

        evaluate(filePath)

def evaluate(dir):
    with open(f"{dir}", "r") as archivo:
        datos = json.load(archivo)

    modelName = None

    similitudSum = 0
    for clave in datos:
        # print("Nombre del contenedor: ", clave)
        if modelName == None:
            modelName = datos[clave]["Model"]

        recognizedText = datos[clave]["Reco"]
        realText = datos[clave]["Real"]

        similitud = difflib.SequenceMatcher(None, recognizedText, realText).ratio()
        similitudSum += similitud
    

    similitudSum =  similitudSum/len(datos)

    print(f"The model \"{modelName}\" has got {similitudSum*100:.2f}% of success.")


def main():
    parser = argparse.ArgumentParser(description='Flags for models results evaluation.')

    #OPCION PARA CREAR Y LIMPIAR

    parser.add_argument('-folder','--folderPath', type=str, help='json full folder path of models results.', default = None)

    args = parser.parse_args()

    error = 0
    folderPath =  None
    if args.folderPath is not None:
        folderPath = args.folderPath
    else:
        error = 1
    
    #En caso de que no se defina alguna obligatoria
    if(error == 1):
        errorMessage()
        return    

    evaluateFolderResults(folderPath)
    
    return

if __name__ == "__main__":
    main()