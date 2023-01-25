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
#TODO lanzar llamada de entrentamiento desde pyton con numero de iteraciones como parametro.

#hacer que el docker copie las fuentes de Fonts, en /usr/local/share/fonts y las regirstre 

#crear groundtruth con un archivo indicando el lenguaje y la fuente
# y otro archivo que indique lenguaje y fuente y mueva las carpetas  


#volver a verme el video

def createGroundTruth(lenguage, font_Name):
    count = 100

    training_text_file = f'langdata/{lenguage}.training_text'

    lines = []

    with open(training_text_file, 'r') as input_file:
        for line in input_file.readlines():
            lines.append(line.strip())

    output_directory = f'tesstrain/data/{font_Name}-ground-truth'

    if not os.path.exists(output_directory):
        os.mkdir(output_directory)

    random.shuffle(lines)

    lines = lines[:count]

    line_count = 0  
    training_text_file_name = pathlib.Path(training_text_file).stem
    for line in lines:
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
            f'--unicharset_file=langdata/{lenguage}.unicharset'
        ])

        line_count += 1

def main():

    lenguage = 'eng' #sys.argv[1]
    font_Name = 'Apex' # sys.argv[2]
    
    lenguageTrainingDataFolder = '/home/tesseract_repos/langdata_lstm'
    tesstrainFolder = '/home/tesseract_repos/tesstrain'
    lenguageTrainingDataFolder = '/home/tesseract_repos/langdata_lstm'

    createGroundTruth(lenguage, font_Name)

if __name__ == "__main__":
    main()