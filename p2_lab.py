import time
from itertools import product
from multiprocessing import Pool

def obtener_contraseña():
    vocales = ['a', 'e', 'i', 'o', 'u']
    combinaciones = product(vocales, repeat=3)  # Generar todas las combinaciones posibles de 3 letras

    for combinacion in combinaciones:
        if combinacion[0] in vocales[:2]:  # Verificar si las dos primeras letras son vocales
            contraseña = ''.join(combinacion)
            return contraseña

# Método de fuerza bruta en serie
start_time = time.time()
contraseña_serial = obtener_contraseña()
end_time = time.time()

tiempo_ejecucion_serial = end_time - start_time
print("Contraseña serial:", contraseña_serial)
print("Tiempo de ejecución en serie:", tiempo_ejecucion_serial)

# Método de fuerza bruta en paralelo
def verificar_contraseña(vocal):
    vocales = [vocal] + ['a', 'e', 'i', 'o', 'u']
    combinaciones = product(vocales, repeat=2)  # Generar todas las combinaciones posibles de las dos últimas letras

    for combinacion in combinaciones:
        contraseña = vocal + ''.join(combinacion)
        if contraseña == contraseña_serial:
            return contraseña

start_time = time.time()
with Pool(processes=5) as pool:
    resultados = pool.map(verificar_contraseña, ['a', 'e', 'i', 'o', 'u'])

contraseña_paralelo = next(contraseña for contraseña in resultados if contraseña is not None)
end_time = time.time()

tiempo_ejecucion_paralelo = end_time - start_time
print("Contraseña paralelo:", contraseña_paralelo)
print("Tiempo de ejecución en paralelo:", tiempo_ejecucion_paralelo)

assert contraseña_serial == contraseña_paralelo
