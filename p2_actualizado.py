import time
from werkzeug.security import check_password_hash
from multiprocessing import Pool

contrasena_correcta = 'pbkdf2:sha256:260000$rTY0haIFRzP8wDDk$57d9f180198cecb45120b772c1317b561f390d677f3f76e36e0d02ac269ad224'

abecedario = ['a','e','i','o','u']  # Las 5 vocales

def comparar_con_password_correcto(palabra):
    return check_password_hash(contrasena_correcta, palabra)

def encontrar_contrasena_primera_letra(vocal):
    combinaciones = []
    
    # Generar todas las combinaciones posibles con la vocal como primera letra
    for letra1 in [vocal]:
        for letra2 in abecedario:
            for letra3 in abecedario:
                combinacion = letra1 + letra2 + letra3
                combinaciones.append(combinacion)

    # Verificar cada combinación en paralelo
    pool = Pool()
    resultados = pool.map(comparar_con_password_correcto, combinaciones)

    # Encontrar la primera combinación correcta
    for i, resultado in enumerate(resultados):
        if resultado:
            return combinaciones[i]

def encontrar_contrasena():
    # Crear 5 procesos, uno para cada vocal como primera letra
    pool = Pool(processes=5)
    resultados = pool.map(encontrar_contrasena_primera_letra, abecedario)

    # Encontrar la primera contraseña correcta
    for resultado in resultados:
        if resultado:
            return resultado

if __name__ == "__main__":
    start_time = time.time()

    contrasena_encontrada = encontrar_contrasena()

    end_time = time.time()
    execution_time = end_time - start_time

    print("Contraseña encontrada:", contrasena_encontrada)
    print("Tiempo de ejecución:", execution_time, "segundos")
