import os
import random
import pathlib
import subprocess
import shutil

from .Constants import *

class GroundTruth():
    def __init__(self, textPath, textLimit = 100):
        self.textPath_ = textPath
        self.textLimit_ = textLimit

    def setTextPath(self, path):
        self.textPath_ = path

    def setTextLineLimit(self, limit):
        self.textLimit_ = limit

    def create(self, language, font_Name):

        training_text_file = f'{self.textPath_}/{language}.training_text'

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

        #Languages training data.
        output_directory += f'/{language}'

        if not os.path.exists(output_directory):
            os.mkdir(output_directory)

        #Randomize lines position
        random.shuffle(lines)

        #Solo recortamos en caso de que exista tamaño suficiente para ello.
        if(self.textLimit_ != -1 and (len(lines) > self.textLimit_)):
            lines = lines[:self.textLimit_]

        line_count = 0  
        training_text_file_name = pathlib.Path(training_text_file).stem
        for line in lines:
            #Create needded gt.txt to validate data
            line_training_text = os.path.join(output_directory, f'{training_text_file_name}_{line_count}.gt.txt')
            with open(line_training_text, 'w') as output_file:
                output_file.writelines([line])

            file_base_name = f'{language}_{line_count}'

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
                f'--unicharset_file={langdata_lstm_Folder}/{language}/{language}.unicharset'
            ])

            line_count += 1

    def clear(self, language, font_Name):
        # Crea un nombre de carpeta a partir de los argumentos lenguage y font_Name
        folder = f'{font_Name}-ground-truth/{language}'
        
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
            print(f'Such folder with \"{language}\" and \"{font_Name}\" does not exist in {tesstrain_Folder}/data')