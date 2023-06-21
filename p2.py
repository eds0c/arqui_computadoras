import datetime
import threading
import time
from socket import AF_INET, SOCK_DGRAM
import socket
import struct

servidores_ntp = [
    "0.uk.pool.ntp.org",    # Londres (Reino Unido)
    "1.es.pool.ntp.org",    # Madrid (España)
    "0.us.pool.ntp.org",    # Nueva York (Estados Unidos)
    "0.hk.pool.ntp.org",    # Hong Kong
    "0.jp.pool.ntp.org"     # Tokyo (Japón)
]

def get_ntp_time(host):
    timezone_dict = {
        'uk': ['UK', 0 * 3600],
        'es': ['España', 1 * 3600],
        'hk': ['Hong Kong', 8 * 3600],
        'jp': ['Japón', 9 * 3600],
        'us': ['Estados Unidos', -5 * 3600]
    }
    key = ''
    port = 123
    buf = 1024
    address = (host, port)
    msg = b'\x1b' + 47 * b'\0'

    TIME1970 = 2208988800
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

def find_next_opening_country():
    now = datetime.datetime.now()
    target_time = now.replace(hour=8, minute=0, second=0, microsecond=0)

    closest_country = None
    closest_time_diff = float('inf')

    for server in servidores_ntp:
        try:
            country_time = get_ntp_time(server)
            time_diff = target_time - country_time
            if time_diff.total_seconds() > 0 and time_diff < closest_time_diff:
                closest_country = server
                closest_time_diff = time_diff
        except socket.timeout:
            print(f"Timeout: No se pudo obtener la hora de {server}")
        except Exception as e:
            print(f"Error al obtener la hora de {server}: {str(e)}")

    if closest_country:
        print(f"La bolsa de valores más próxima a abrir es en: {closest_country}")
    else:
        print("No se pudo determinar la bolsa de valores más próxima a abrir")

def find_next_opening_country_threads():
    now = datetime.datetime.now()
    target_time = now.replace(hour=8, minute=0, second=0, microsecond=0)

    closest_country = None
    closest_time_diff = float('inf')

    def check_country(server):
        nonlocal closest_country, closest_time_diff
        try:
            country_time = get_ntp_time(server)
            time_diff = target_time - country_time
            if time_diff.total_seconds() > 0 and time_diff < closest_time_diff:
                closest_country = server
                closest_time_diff = time_diff
        except socket.timeout:
            print(f"Timeout: No se pudo obtener la hora de {server}")
        except Exception as e:
            print(f"Error al obtener la hora de {server}: {str(e)}")

    threads = []
    for server in servidores_ntp:
        thread = threading.Thread(target=check_country, args=(server,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    if closest_country:
        print(f"La bolsa de valores más próxima a abrir es en: {closest_country}")
    else:
        print("No se pudo determinar la bolsa de valores más próxima a abrir")

# Parte a)
start_time_a = time.time()
find_next_opening_country()
end_time_a = time.time()
execution_time_a = end_time_a - start_time_a
print(f"Tiempo de ejecución (Parte a): {execution_time_a} segundos")

# Parte b)
start_time_b = time.time()
find_next_opening_country_threads()
end_time_b = time.time()
execution_time_b = end_time_b - start_time_b
print(f"Tiempo de ejecución (Parte b): {execution_time_b} segundos")

if execution_time_a < execution_time_b:
    print("La implementación de la parte a) fue más rápida")
else:
    print("La implementación de la parte b) fue más rápida")