from socket import AF_INET, SOCK_DGRAM
import datetime
import threading
import socket
import struct
import time

servidores_ntp = [
    "0.uk.pool.ntp.org",    # Londres (Reino Unido)
    "1.es.pool.ntp.org",    # Madrid (España)
    "0.us.pool.ntp.org",    # Nueva York (Estados Unidos)
    "0.hk.pool.ntp.org",    # Hong Kong
    "0.jp.pool.ntp.org"     # Tokio (Japón)
]

"""
Función: get_ntp_time
Descripción: Imprime la fecha-hora actual en un país determinado
Entrada: Cualquiera de las URLs definidas en la lista servidores_ntp
Salida: Retorna la fecha-hora (timestamp) en formato datetime.datetime, también la imprime
IMPORTANTE: NO modifique esta función
"""
def get_ntp_time(host):
    timezone_dict = {'uk': ['UK', 0 * 3600], 'es': ['España', 1 * 3600],
                     'hk': ['Hong Kong', 8 * 3600], 'jp': ['Japón', 9 * 3600],
                     'us': ['Estados Unidos', -5 * 3600]}
    key = ''
    port = 123
    buf = 1024
    address = (host, port)
    msg = b'\x1b' + 47 * b'\0'

    # reference time (in seconds since 1900-01-01 00:00:00)
    TIME1970 = 2208988800  # 1970-01-01 00:00:00
    # connect to server
    client = socket.socket(AF_INET, SOCK_DGRAM)
    client.sendto(msg, address)
    msg, address = client.recvfrom(buf)
    t = struct.unpack("!12I", msg)[10]
    t -= TIME1970
    client.close()

    for each_key in timezone_dict:
        if each_key in host:
            key = each_key
            break
    print(f"Hora en {timezone_dict[key][0]}: {datetime.datetime.utcfromtimestamp(t + timezone_dict[key][1])}")
    return datetime.datetime.utcfromtimestamp(t + timezone_dict[key][1])


def encontrar_pais_cercano():
    min_tiempo_restante = float('inf')
    pais_cercano = ""

    for servidor in servidores_ntp:
        hora_servidor = get_ntp_time(servidor)
        tiempo_restante = (hora_servidor - datetime.datetime.now()).total_seconds()

        if tiempo_restante < min_tiempo_restante:
            min_tiempo_restante = tiempo_restante
            pais_cercano = servidor

    print(f"El país cuya bolsa de valores está más próxima a abrir es: {pais_cercano}")
    print(f"Tiempo de ejecución: {time.process_time()}")


def encontrar_pais_cercano_threads():
    min_tiempo_restante = float('inf')
    pais_cercano = ""
    lock = threading.Lock()

    def consultar_ntp(servidor):
        nonlocal min_tiempo_restante, pais_cercano

        hora_servidor = get_ntp_time(servidor)
        tiempo_restante = (hora_servidor - datetime.datetime.now()).total_seconds()

        with lock:
            if tiempo_restante < min_tiempo_restante:
                min_tiempo_restante = tiempo_restante
                pais_cercano = servidor

    threads = []

    for servidor in servidores_ntp:
        thread = threading.Thread(target=consultar_ntp, args=(servidor,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    print(f"El país cuya bolsa de valores está más próxima a abrir es: {pais_cercano}")
    print(f"Tiempo de ejecución: {time.process_time()}")


if __name__ == '__main__':
    print("---- Tarea a) ----")
    start_time_a = time.process_time()
    encontrar_pais_cercano()
    end_time_a = time.process_time()
    print(f"Tiempo de ejecución de la tarea a): {end_time_a - start_time_a}")

    print("---- Tarea b) ----")
    start_time_b = time.process_time()
    encontrar_pais_cercano_threads()
    end_time_b = time.process_time()
    print(f"Tiempo de ejecución de la tarea b): {end_time_b - start_time_b}")
