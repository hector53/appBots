import socket

# Dirección del socket
socket_path = "/tmp/python_unix_socket"

client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
client.connect(socket_path)

try:
    message = 'Hola, servidor!'
    print("Enviando:", message)
    client.sendall(message.encode())

    response = client.recv(1024)
    print("Recibido:", response.decode())
finally:
    client.close()
