import os
import random
import pathlib
import subprocess
import sys
import shutil

import argparse

#TODO borrar user-patterns y user-words de tesseract/tessdata a ver si funciona
#TODO leer parametros de entrada para empezar a entrenar


#TODO que el ground truth este en otro sitio, COMO DEMONIOS SABE QUE PARA ENTRENAR EL GROUNDTRUTH ESTA EN testrain/data? BUA IGUAL EL NOMBREDE NO PUEDE SER APex-eng-ground-truth
#igual tengo que crear la carpeta y meterlo ahi, cague

#volver a verme el video

langdata_lstm_Folder = '/home/tesseract_repos/langdata_lstm'
tessdata_best_Folder = '/home/tesseract_repos/tessdata_best'
tesstrain_Folder = '/home/tesseract_repos/tesstrain'
tesseract_Folder = '/home/tesseract_repos/tesseract'

def createGroundTruth(lenguage, font_Name, path):
    count = 200

    training_text_file = f'{path}/{lenguage}.training_text'

    #Array with training lines data
    lines = []

    with open(training_text_file, 'r') as input_file:
        for line in input_file.readlines():
            lines.append(line.strip())

    #Output directory creation
    output_directory = f'{tesstrain_Folder}/data'

    if not os.path.exists(output_directory):
        os.mkdir(output_directory)

    #Font folder that stores all training information.
    output_directory += f'/{font_Name}_data'

    if not os.path.exists(output_directory):
        os.mkdir(output_directory)

    #Ground Truth Directory with all lenguages training data.
    output_directory += f'/{font_Name}-ground-truth'
    
    if not os.path.exists(output_directory):
        os.mkdir(output_directory)

    #Lenguages training data.
    output_directory += f'/{lenguage}'

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


def clear(lenguage, font_Name):
    # Crea un nombre de carpeta a partir de los argumentos lenguage y font_Name
    folder = f'{font_Name}-ground-truth/{lenguage}'
    
    # Crea una ruta completa para la carpeta
    completeFolder = f'{tesstrain_Folder}/data/{font_Name}_data/' + folder
    
    # Verifica si la carpeta existe
    if os.path.exists(completeFolder):
        # Elimina la carpeta y todo su contenido
        shutil.rmtree(completeFolder)
        
        # Mensaje de éxito
        print(f'\033[32mFolder {folder} succesfully removed.\033[0m')
    else:
        # Mensaje indicando que la carpeta no existe
        print(f'Such folder with \"{lenguage}\" and \"{font_Name}\" does not exist in {tesstrain_Folder}/data')

def main():
    parser = argparse.ArgumentParser(description='Flags for flags in ground truth.')

    #OPCION PARA CREAR Y LIMPIAR

    parser.add_argument('-dir','--directory', type=str, help='Directory name with training text.', default = None)
    parser.add_argument('-l','--lenguage', type=str, help='Lenguage name.', default = None)
    parser.add_argument('-f','--fontname', type=str, help='Font name.', default = None)
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

    #En caso de que no se defina alguna obligatoria
    if(error == 1):
        print("\033[31mYou must provide at least lenguage and font name.\033[0m")
        print("\033[36Usage: python groundTruth.py -l [lenguaje] -f [fontName]\033[0m")
        return 

    #En caso de que se especifique limpiar
    if args.clear is not False:
        clear(lenguage, font_Name)
        return

    #Ruta por defecto
    path = f'{langdata_lstm_Folder}/{lenguage}'

    #Ruta personalizada
    if args.directory is not None:
        path = args.directory 

    
    
    createGroundTruth(lenguage, font_Name,path)

if __name__ == "__main__":
    main()