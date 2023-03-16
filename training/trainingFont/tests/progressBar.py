from tqdm import tqdm
import time
import subprocess 
# for i in tqdm(range(100)):
#     time.sleep(0.1)

def function_A(func=None):
    if func is None:
        print("El argumento es None")
    else:
        func()

function_A() # Output: El argumento es None

function_B = lambda: print("Hola, soy la función B")

function_A(func=function_B) # Output: Hola, soy la función B
