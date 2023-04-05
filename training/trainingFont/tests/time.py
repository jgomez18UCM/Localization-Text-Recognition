import time
import datetime

def metodo(n):
    numeros = []

    for i in range(1, n):
        numeros.append(i)

start_time = time.time()

# Aquí va tu método
metodo(100)

end_time = time.time()
elapsed_time = end_time - start_time

# Creamos un objeto datetime a partir de la diferencia de tiempo
delta_time = datetime.datetime.utcfromtimestamp(elapsed_time)

# Formateamos el objeto datetime en minutos, segundos y milisegundos utilizando strftime
print("Tiempo transcurrido: {}".format(delta_time.strftime('%H:%M:%S.%f')))