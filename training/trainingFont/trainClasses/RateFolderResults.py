import os
import difflib
import json

class RateFolderResults():
    def __init__(self, folder):
        self.folder_ = folder

    def setFolder(self, folder):
        self.folder_ = folder

    def rateFile(self, dir):
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

        #Imprimir en pantalla los resultados, con el nombre del modelo y porcentaje de acierto subrayado.
        print(f"The model \033[1m\033[4m\"{modelName}\"\033[0m has got \033[1m\033[4m{similitudSum*100:.2f}%\033[0m of success.")
    
    def rateFolder(self):
        if self.folder_ == None:
            print("Models results json folder path is None.")
            return
        
        if not os.path.exists(self.folder_):
            print("Such folder does not exist.")
            return

        folder = os.listdir(self.folder_)
        for file in folder:
            filePath = None
            if(not self.folder_.endswith("/")):
                filePath = self.folder_ +"/"+ file
            else:
                filePath = self.folder_ + file

            self.rateFile(filePath)