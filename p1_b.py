import time
from multiprocessing import Pool

def calcular_termino(i, x):
    return i * (x ** i)

def calcular_f_paralelo(x):
    n = 10000
    procesos = 4
    terminos_por_proceso = n // procesos

    with Pool(processes=procesos) as pool:
        resultados = []

        for i in range(procesos):
            inicio = i * terminos_por_proceso + 1
            fin = inicio + terminos_por_proceso

            if i == procesos - 1:
                fin = n + 1

            resultados.append(pool.apply_async(calcular_termino, args=(x,)))

        suma = sum([resultado.get() for resultado in resultados])

    return suma

# Calcular f(2023) en paralelo
start_time = time.time()
resultado_paralelo = calcular_f_paralelo(2023)
end_time = time.time()

tiempo_ejecucion_paralelo = end_time - start_time
print("Resultado paralelo:", resultado_paralelo)
print("Tiempo de ejecución en paralelo:", tiempo_ejecucion_paralelo)
