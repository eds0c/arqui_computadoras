import threading
import socket

# Definir constantes
HOST = 'localhost'
PORT = 12345

# Función para recibir datos del servidor
def recibir_datos(server_socket):
    while True:
        data = server_socket.recv(1024).decode()
        if not data:
            break
        procesar_datos(data)

    server_socket.close()

# Función para procesar los datos recibidos
def procesar_datos(data):
    row = data.split(',')
    precio_unitario = float(row[5])
    cantidades = int(row[3])
    costo_total = precio_unitario * cantidades

    if costo_total < 25:
        clasificacion = 'Costo bajo'
    elif 25.0 <= costo_total < 50.0:
        clasificacion = 'Costo regular'
    elif 50.0 <= costo_total < 75.0:
        clasificacion = 'Costo alto'
    else:
        clasificacion = 'Costo elevado'

    global contador_costo_elevado
    global contador_peso_elevado
    global contador_costo_bajo

    if clasificacion == 'Costo elevado':
        contador_costo_elevado += 1
        if float(row[4]) > 100.0:
            contador_peso_elevado += 1
    elif clasificacion == 'Costo bajo':
        contador_costo_bajo += 1

    print(f'Datos recibidos: {data}')
    print(f'Costo total: {costo_total}')
    print(f'Clasificación: {clasificacion}')
    print(f'Contador costo elevado: {contador_costo_elevado}')
    print(f'Contador peso elevado: {contador_peso_elevado}')
    print(f'Contador costo bajo: {contador_costo_bajo}')
    print('')

# Inicializar los contadores
contador_costo_elevado = 0
contador_peso_elevado = 0
contador_costo_bajo = 0

# Función principal para el segundo thread
def thread_cliente():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((HOST, PORT))

    recibir_datos(server_socket)

# Iniciar el segundo thread
cliente_thread = threading.Thread(target=thread_cliente)
cliente_thread.start()