"""
server.py:

    Se crea un sochet del servidor, que se ejecuta cuando se inicia el servidor.
    Una vez conectado al cliente (se ejecuta por consola), envía un mensaje de bienvenida y dos opciones de consulta.
    El servidor retorna la información solicitada, consultando a la base de datos correspondiente.
"""


from connector import LogObserver1, LogObserver2
import socket
import datetime


def lanzar_server():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()  # Esta es la IP del servidor
    puerto = 456  # Puerto en el cual estoy escuchado
    print(host)

    # para asociar un socket a una dirección de servidor
    serversocket.bind((host, puerto))
    serversocket.listen(3)    # para escuchar
    print("El servidor esta encendido")

    while True:
        # Aceptar una conexión
        client_socket, addr = serversocket.accept()
        print(f"Conexión aceptada de {addr}")

        # Enviar mensaje de bienvenida y menú de opciones
        mensaje_inicio = '''\t¡Bienvenido al servidor!
        Para obtener detalles de dia de hoy, por favor elija una opción:
        1. Base de datos seleccionada
        2. Métodos utilizados
        3. Salir\n'''
        client_socket.sendall(mensaje_inicio.encode('utf-8'))

        while True:
            # Recibir la selección del cliente
            data = client_socket.recv(1024).decode('utf-8')
            # print(data)
            # print(type(data))
            if not data:
                break

            # Procesar la opción seleccionada
            response = "Opción no válida."
            if data == '1':
                today = datetime.datetime.now().strftime("%Y-%m-%d")
                print(today)
                events = LogObserver1.select().where(
                    LogObserver1.date >= today)
                if events:
                    response = "Eventos del día de hoy:\n"
                    for event in events:
                        response += f"{event.motivo}: {event.tipo_base}\n"
                        # print(response)
                else:
                    response = "No hay eventos para hoy."
            if data == '2':
                today = datetime.datetime.now().strftime("%Y-%m-%d")
                print(today)
                events = LogObserver2.select().where(
                    LogObserver2.date >= today)
                if events:
                    response = "Eventos del día de hoy:\n"
                    for event in events:
                        response += f"{event.metodo}: {event.identificador}, {event.description}\n"
                        # print(response)
                else:
                    response = "No hay eventos para hoy."
            elif data == '3':
                response = "Saliendo..."
                client_socket.sendall(response.encode('utf-8'))
                break

            print(response)

            # Enviar la respuesta al cliente
            client_socket.sendall(response.encode('utf-8'))
        client_socket.close()
