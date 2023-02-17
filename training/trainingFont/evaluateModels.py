from sklearn.model_selection import KFold
import numpy as np
import os
import shutil


def move():
    # Ruta de la carpeta original
    ruta_original = "ruta/a/la/carpeta/original"
    # Ruta de la carpeta de destino
    ruta_destino = "ruta/a/la/carpeta/de/destino"

    # Obtener la lista de archivos en la carpeta original
    archivos = os.listdir(ruta_original)

    # Calcular el número de archivos que corresponden al 1/5 de la lista
    num_archivos_1_5 = len(archivos) // 5

    # Mover los primeros 1/5 de los archivos a la carpeta de destino
    for archivo in archivos[:num_archivos_1_5]:
        origen = os.path.join(ruta_original, archivo)
        destino = os.path.join(ruta_destino, archivo)
        shutil.move(origen, destino)

    # Devolver los archivos a la carpeta original
    for archivo in os.listdir(ruta_destino):
        origen = os.path.join(ruta_destino, archivo)
        destino = os.path.join(ruta_original, archivo)
        shutil.move(origen, destino)

    # Mover los siguientes 1/5 de los archivos a la carpeta de destino
    for archivo in archivos[num_archivos_1_5:2*num_archivos_1_5]:
        origen = os.path.join(ruta_original, archivo)
        destino = os.path.join(ruta_destino, archivo)
        shutil.move(origen, destino)

    # Devolver los archivos a la carpeta original
    for archivo in os.listdir(ruta_destino):
        origen = os.path.join(ruta_destino, archivo)
        destino = os.path.join(ruta_original, archivo)
        shutil.move(origen, destino)        

def main():
    # Generar datos de ejemplo
    X = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])
    y = np.array([1, 2, 3, 4])

    # Crear objeto KFold
    kf = KFold(n_splits=4)

    # Iterar sobre los índices de entrenamiento y prueba en cada iteración de k-folding
    for train_index, test_index in kf.split(X):
        print("Índices de entrenamiento:", train_index, "Índices de prueba:", test_index)
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]

        print("Datos de entrenamiento:")
        print("X:", X_train)
        print("Y:", y_train)

        print("Datos de prueba:")
        print("X:", X_test)
        print("Y:", y_test)

    return

if __name__ == "__main__":
    main()