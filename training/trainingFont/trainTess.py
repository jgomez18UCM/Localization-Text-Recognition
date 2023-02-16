import os
import random
import pathlib
import subprocess
import sys

import argparse 

#TODO borrar user-patterns y user-words de tesseract/tessdata a ver si funciona
#TODO leer parametros de entrada para empezar a entrenar
#TODO si ya se ha generado el ground-truth que no se haga de nuevo
#TODO que el ground truth este en otro sitio, COMO DEMONIOS SABE QUE PARA ENTRENAR EL GROUNDTRUTH ESTA EN testrain/data?

langdata_lstm_Folder = '/home/tesseract_repos/langdata_lstm'
tessdata_best_Folder = '/home/tesseract_repos/tessdata_best'
tesstrain_Folder = '/home/tesseract_repos/tesstrain'
tesseract_Folder = '/home/tesseract_repos/tesseract'

def trainOCR(lenguage, font_Name,maxIterations):
    
    groundTruthPath = f'{tesstrain_Folder}/data/{font_Name}-ground-truth/{lenguage}'

    if (not os.path.exists(groundTruthPath)):
        print("ERROR!")
        print(f"There is no ground truth for \"{font_Name}\" and \"{lenguage}\" lenguage!")
        return
    
    #We get main launch directory so we can turn back
    mainLaunchDir = os.getcwd()
    #We need to launch the command in tesseract folder so it can access auxiliar files
    #in its repository
    os.chdir(f'{tesstrain_Folder}')

    #Launch training from tesseract folder
    subprocess.run([
            'make',
            '-f',
            f'{tesstrain_Folder}/Makefile',
            'training',
            f'TESSDATA_PREFIX={tesseract_Folder}/tessdata',
            f'MODEL_NAME={font_Name}',  
            f'START_MODEL={lenguage}',
            f'GROUND_TRUTH_DIR = {tesstrain_Folder}/data/{font_Name}-ground-truth/{lenguage}',
            f'TESSDATA={tesseract_Folder}/tessdata',
            f'MAX_ITERATIONS={maxIterations}',
        ])

    #Come back to main execution folder.
    os.chdir(f'{mainLaunchDir}')

    if not os.path.exists(f'{mainLaunchDir}/trainedModel'):
        os.mkdir(f'{mainLaunchDir}/trainedModel')

    #Copy trained model to mainFolder
    subprocess.run(['cp','-f', '--recursive',f'{tesstrain_Folder}/data/{font_Name}.traineddata', f'{mainLaunchDir}/trainedModel'])

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
        lenguage = args.lenguage
    else:
        error = 1
    
    if args.fontname is not None:
        font_Name = args.fontname
    else:
        error = 1

    if args.iterations is not None:
        maxIterations = args.iterations
    else:
        error = 1

    #En caso de que no se defina alguna obligatoria
    if(error == 1):
        print("ERROR!")
        print("You must provide at least lenguage, font name and a number of iterations.")
        print("Usage: python trainTess.py -l [lenguaje] -f [fontName] -it [natural number]")
        return

    # lenguage = sys.argv[1] #'eng'
    # font_Name = sys.argv[2] #'Apex' 
    # maxIterations = sys.argv[3] #'1000' 

    #Mover de tessdata_best a /home/tetesseract_repos/langdata los trainneddata
    subprocess.run(['cp', '-n',f'{tessdata_best_Folder}/{lenguage}.traineddata',  f'{tesseract_Folder}/tessdata'])

    trainOCR(lenguage, font_Name, maxIterations)

if __name__ == "__main__":
    main()