import time
import math
from multiprocessing import Process

def es_primo(n):
    if n < 2:
        return False

    limite = int(math.sqrt(n)) + 1

    for i in range(2, limite):
        if n % i == 0:
            return False

    return True

# Implementación serial
def verificar_primo_serial(n):
    start_time = time.time()
    resultado = es_primo(n)
    end_time = time.time()
    tiempo_ejecucion = end_time - start_time

    print("Resultado serial:", resultado)
    print("Tiempo de ejecución en serie:", tiempo_ejecucion)

    return resultado

# Implementación paralela
def verificar_primo_paralelo(n):
    start_time = time.time()

    procesos = []
    resultado = False

    def verificar_primo(numero):
        nonlocal resultado
        resultado = es_primo(numero)

    proceso1 = Process(target=verificar_primo, args=(n,))
    proceso2 = Process(target=verificar_primo, args=(n + 2,))

    procesos.append(proceso1)
    procesos.append(proceso2)

    for proceso in procesos:
        proceso.start()

    for proceso in procesos:
        proceso.join()

    end_time = time.time()
    tiempo_ejecucion = end_time - start_time

    print("Resultado paralelo:", resultado)
    print("Tiempo de ejecución en paralelo:", tiempo_ejecucion)

    return resultado

# Parte a)
print("Parte a)")
verificar_primo_serial(2345678911111111)

# Parte b)
print("\nParte b)")
resultado_serial = verificar_primo_serial(2345678911111111)
resultado_paralelo = verificar_primo_paralelo(2345678911111111)

assert resultado_serial == resultado_paralelo

# Parte c)
print("\nParte c)")

def encontrar_siguiente_primo(X):
    while True:
        proceso1 = Process(target=verificar_primo, args=(X + 1,))
        proceso2 = Process(target=verificar_primo, args=(X + 3,))

        proceso1.start()
        proceso2.start()

        proceso1.join()
        proceso2.join()

        if es_primo(X + 1):
            print("El siguiente número primo encontrado es", X + 1)
            break

        if es_primo(X + 3):
            print("El siguiente número primo encontrado es", X + 3)
            break

        X += 4

encontrar_siguiente_primo(24)
