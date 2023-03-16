from tqdm import tqdm
import time
import subprocess 
# for i in tqdm(range(100)):
#     time.sleep(0.1)

def aplicar_funcion(funcion):
    print("Goint to exec")
    if funcion is not None:
        print("Exec")
        funcion()
    else:
        print("Is None")

# Llamando a la función y pasando una lambda como argumento
# resultado = aplicar_funcion(lambda: subprocess.run(['mkdir', 'holaComoEstas']))
resultado = aplicar_funcion(lambda:None)