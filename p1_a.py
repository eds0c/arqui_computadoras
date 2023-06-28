import time

def calcular_f_serial(x):
    n = 10000
    suma = 0

    for i in range(1, n+1):
        termino = i * (x ** i)
        suma += termino

    return suma

# Calcular f(2023) en serie
start_time = time.time()
resultado_serial = calcular_f_serial(2023)
end_time = time.time()

tiempo_ejecucion_serial = end_time - start_time
print("Resultado serial:", resultado_serial)
print("Tiempo de ejecución en serie:", tiempo_ejecucion_serial)
