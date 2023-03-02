import json

with open("datos.json", "r") as archivo:
    datos = json.load(archivo)

for clave in datos:
    print("Nombre del contenedor: ", clave)
    print("Modelo: ", datos[clave]["Model"])
    print("Reco: ", datos[clave]["Reco"])
    print("Real: ", datos[clave]["Real"])
    print()