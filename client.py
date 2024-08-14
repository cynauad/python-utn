"""
client.py:

    Se crea un sochet de cliente que se ejecuta por consola.
    Una vez conectado al servidor (app), este último envia dos opciones de consulta 
    sobre la base de datos del modelo observador.
    Desde el cliente se envia al servidor la opción seleccionada y luego el servidor retorna
    la información solicitada.
"""


import socket


def main():
    # Crear un socket de cliente

    host = socket.gethostbyname(socket.gethostname())  # 'localhost'
    puerto = 456
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, puerto))               # realiza la conexion

    while True:
        # Recibe y muestra el mensaje del servidor
        mensaje = client.recv(1024).decode('utf-8')
        print(mensaje)

        if "Saliendo..." in mensaje:
            break

        # Envia la opción seleccionada al servidor
        option = input("Selecciona una opción (1-3): ")
        client.send(option.encode('utf-8'))

    # Cierra la conexión con el servidor
    client.close()


if __name__ == "__main__":
    main()
