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

#volver a verme el video

langdata_lstm_Folder = '/home/tesseract_repos/langdata_lstm'
tessdata_best_Folder = '/home/tesseract_repos/tessdata_best'
tesstrain_Folder = '/home/tesseract_repos/tesstrain'
tesseract_Folder = '/home/tesseract_repos/tesseract'

def createGroundTruth(lenguage, font_Name, path):
    count = 100

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

def main():
    parser = argparse.ArgumentParser(description='Example program for parsing flags.')

    #OPCION PARA CREAR Y LIMPIAR

    parser.add_argument('-d','--dir', type=str, help='Directory name with training text.', default = None)
    parser.add_argument('-l','--lenguage', type=str, help='Lenguage name.', default = None)
    parser.add_argument('-f','--fontname', type=str, help='Font name.', default = None)
    # parser.add_argument('--limitLines', type=int, help='Number of limit lines. By default there is no limit.')

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

    if(error == 1):
        print("ERROR!")
        print("You must provide at least lenguage and font name.")
        print("Usage: python createGroundTruth.py -l [lenguaje] -f [fontName]")
        return 

    
    path = f'{langdata_lstm_Folder}/{lenguage}'

    if args.dir is not None:
        path = args.dir 

    # print("Directory:", args.dir)
    # print("Lenguage:", args.lenguage)
    # print("Fontname:", args.fontname)

    createGroundTruth(lenguage, font_Name,path)

if __name__ == "__main__":
    main()