import os
import random
import pathlib
import subprocess
import sys

# import argparse ? 

#TODO borrar user-patterns y user-words de tesseract/tessdata a ver si funciona
#TODO leer parametros de entrada para empezar a entrenar
#TODO si ya se ha generado el ground-truth que no se haga de nuevo
#TODO que el ground truth este en otro sitio, COMO DEMONIOS SABE QUE PARA ENTRENAR EL GROUNDTRUTH ESTA EN testrain/data?

#volver a verme el video

langdata_lstm_Folder = '/home/tesseract_repos/langdata_lstm'
tessdata_best_Folder = '/home/tesseract_repos/tessdata_best'
tesstrain_Folder = '/home/tesseract_repos/tesstrain'
tesseract_Folder = '/home/tesseract_repos/tesseract'

def createGroundTruth(lenguage, font_Name):
    count = 100

    training_text_file = f'{langdata_lstm_Folder}/{lenguage}/{lenguage}.training_text'

    #Array with training lines data
    lines = []


    with open(training_text_file, 'r') as input_file:
        for line in input_file.readlines():
            lines.append(line.strip())

    #Output directory creation
    output_directory = f'{tesstrain_Folder}/data'

    if not os.path.exists(output_directory):
        os.mkdir(output_directory)

    output_directory += f'/{font_Name}-ground-truth'
    
    if not os.path.exists(output_directory):
        os.mkdir(output_directory)

    #Randomize lines position
    random.shuffle(lines)

    lines = lines[:count]

    line_count = 0  
    training_text_file_name = pathlib.Path(training_text_file).stem
    for line in lines:
        #Create needded gt.txt to validate data
        line_training_text = os.path.join(output_directory, f'{training_text_file_name}_{line_count}.gt.txt')
        with open(line_training_text, 'w') as output_file:
            output_file.writelines([line])

        file_base_name = f'{lenguage}_{line_count}'

        subprocess.run([
            'text2image',
            f'--font={font_Name}',
            f'--text={line_training_text}',
            f'--outputbase={output_directory}/{file_base_name}',
            '--max_pages=1',
            '--strip_unrenderable_words',
            '--leading=32',
            '--xsize=3600',
            '--ysize=480',
            '--char_spacing=1.0',
            '--exposure=0',
            f'--unicharset_file={langdata_lstm_Folder}/{lenguage}/{lenguage}.unicharset'
        ])

        line_count += 1

def trainOCR(lenguage, font_Name,maxIterations):
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
    lenguage = sys.argv[1] #'eng'
    font_Name = sys.argv[2] #'Apex' 
    maxIterations = sys.argv[3] #'1000' 

    #Prepare all necessary files in corresponding foldes    
    #Mover de langdata_lstm  a /home/tetesseract_repos/tesseract/tessdata la carpeta entera del lenguaje
    # subprocess.run(['cp','-n', '--recursive',f'{langdata_lstm_Folder}/{lenguage}', trainingCurrLangData])
    
    #Mover de tessdata_best a /home/tetesseract_repos/langdata los trainneddata
    subprocess.run(['cp', '-n',f'{tessdata_best_Folder}/{lenguage}.traineddata',  f'{tesseract_Folder}/tessdata'])

    createGroundTruth(lenguage, font_Name)

    trainOCR(lenguage, font_Name, maxIterations)

if __name__ == "__main__":
    main()