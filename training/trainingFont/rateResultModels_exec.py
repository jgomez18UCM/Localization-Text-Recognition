import argparse

from trainClasses.RateFolderResults import RateFolderResults

def errorMessage():
    print("\033[31mYou must provide models results json full folder path .\033[0m")
    print("\033[36mUsage: python evaluateResultsModels.py -folder [folderPath]\033[0m")

def main():
    parser = argparse.ArgumentParser(description='Flags for models results evaluation.')

    #OPCION PARA CREAR Y LIMPIAR

    parser.add_argument('-dir','--directoryPath', type=str, help='JSON complete-folder-path of models results.', default = None)

    args = parser.parse_args()

    error = 0
    folderPath =  None
    if args.directoryPath is not None:
        folderPath = args.directoryPath
    else:
        error = 1
    
    #En caso de que no se defina alguna obligatoria
    if(error == 1):
        errorMessage()
        return    

    rateInstance = RateFolderResults(folderPath)
    rateInstance.rateFolder()
    
    return

if __name__ == "__main__":
    main()