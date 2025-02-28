import socket
from threading import Thread
from ults import get_info_server, server_main_process

DEFAUT_ADMIN_KEY = 'private'
host, port, buffer, admin_key = get_info_server(DEFAUT_ADMIN_KEY)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host, port))
sock.listen(10)
print(f'server {host}:{port} listening')
server_main_process(sock, buffer, admin_key)
