import threading
import csv
import time
import socket

# Definir constantes
HOST = 'localhost'
PORT = 12345
FILE_PATH = 'PartesDeElectrónica.csv'

# Función para leer el archivo CSV
def leer_archivo_csv():
    with open(FILE_PATH, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Saltar la cabecera
        for row in reader:
            yield row

# Función para enviar datos al cliente
def enviar_datos(client_socket):
    for row in leer_archivo_csv():
        data = ','.join(row)
        client_socket.send(data.encode())
        time.sleep(1)

# Función principal para el primer thread
def thread_servidor():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print('Servidor en espera de conexión...')

    client_socket, client_address = server_socket.accept()
    print(f'Conexión establecida con {client_address}')

    enviar_datos(client_socket)

    client_socket.close()
    server_socket.close()

# Iniciar el primer thread
servidor_thread = threading.Thread(target=thread_servidor)
servidor_thread.start()
