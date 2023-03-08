import argparse
import json
import difflib

def errorMessage():
    print("\033[31mYou must provide models results json file path .\033[0m")
    print("\033[36mUsage: python evaluateResultsModels.py -file [filePath]\033[0m")

def evaluate(dir):
    with open(f"{dir}", "r") as archivo:
        datos = json.load(archivo)

    modelName = None

    similitudSum = 0
    for clave in datos:
        if modelName == None:
            modelName = datos[clave]["Model"]

        recognizedText = datos[clave]["Reco"]
        realText = datos[clave]["Real"]

        similitud = difflib.SequenceMatcher(None, recognizedText, realText).ratio()
        similitudSum += similitud
    

    similitudSum =  similitudSum/len(datos)

    print(f"The model \"{modelName}\" has got {similitudSum*100:.2f}% of success")


def main():
    parser = argparse.ArgumentParser(description='Flags for models results evaluation.')

    #OPCION PARA CREAR Y LIMPIAR

    parser.add_argument('-file','--filePath', type=str, help='json file path of models results.', default = None)

    args = parser.parse_args()

    error = 0
    filePath =  None
    if args.filePath is not None:
        filePath = args.filePath
    else:
        error = 1
    
    #En caso de que no se defina alguna obligatoria
    if(error == 1):
        errorMessage()
        return    

    evaluate(filePath)
    
    return

if __name__ == "__main__":
    main()