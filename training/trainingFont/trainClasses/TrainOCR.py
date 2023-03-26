import os
import subprocess
import shutil

from .Constants import *

class TrainOCR():
    def __init__(self):
        pass

    def train(self, language, font_Name, iterations = 100):
        groundTruthPath = f'{tesstrain_Folder}/data/{font_Name}_data/{font_Name}-ground-truth/{language}'

        if (not os.path.exists(groundTruthPath)):
            print(f"WARNING : There is no ground-truth for \"{font_Name}\" and \"{language}\" language!")
            print(f"Please make sure you generate a ground-truth for \"{font_Name}\" and \"{language}\".")
            return
        
        #Folder to store temporary training data
        output_directory =  f'{tesstrain_Folder}/data/{font_Name}_data/{font_Name}-{language}-output'
        if not os.path.exists(output_directory):
            os.mkdir(output_directory)

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
                f'START_MODEL={language}',
                f'GROUND_TRUTH_DIR = {tesstrain_Folder}/data/{font_Name}_data/{font_Name}-ground-truth/{language}',
                f'TESSDATA={tesseract_Folder}/tessdata',
                f'DATA_DIR= {output_directory}',
                f'MAX_ITERATIONS={iterations}',
            ])

        #Come back to main execution folder.
        os.chdir(f'{mainLaunchDir}')

        if not os.path.exists(f'{mainLaunchDir}/trainedModel'):
            os.mkdir(f'{mainLaunchDir}/trainedModel')

        #Copy trained model to mainFolder
        subprocess.run(['cp','-f', '--recursive',f'{output_directory}/{font_Name}.traineddata', f'{mainLaunchDir}/trainedModel'])
    
    def clear(self,language, font_Name):
        # Crea un nombre de carpeta a partir de los argumentos lenguage y font_Name
        folder = f'{font_Name}-{language}-output/'
        
        # Crea una ruta completa para la carpeta
        completeFolder = f'{tesstrain_Folder}/data/{font_Name}_data/' + folder
        
        # Verifica si la carpeta existe
        if os.path.exists(completeFolder):
            # Elimina la carpeta y todo su contenido
            shutil.rmtree(completeFolder)
            
            # Mensaje de éxito
            print(f'\033[32mFolder {folder} with training data succesfully removed.\033[0m')
        else:
            # Mensaje indicando que la carpeta no existe
            print(f'Such folder with {language} and {font_Name} does not exist in {tesstrain_Folder}/data')