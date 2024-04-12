import socket
import os
import pickle
import threading

HOST = ""
PORT = 9090

TYPE = socket.AF_INET
PROTOCOL = socket.SOCK_STREAM

folder = "f_main"
directory = os.path.join(os.getcwd(), folder)


def client_processing(sock, addr):
    try:
        received_data = b''
        fl = False
        while True:
            if fl:
                sock.settimeout(2.0)
                try:

                    pal = sock.recv(1)
                    received_data += pal
                except socket.timeout:
                    break
            else:
                pal = sock.recv(1)
                fl = True
                if not pal:
                    break
                received_data += pal
        # client_socket.send(command.encode())
        # packageLen = int(client_socket.recv(1024).decode())
        # bytesReceive = 0
        # response = b''
        #
        # while bytesReceive < packageLen:
        #     chunk = client_socket.recv(min(packageLen - bytesReceive, 2048))
        #     bytesReceive = bytesReceive + len(chunk)
        #     response += chunk
        print(f"Received from {addr}")
        received_data = pickle.loads(received_data)
        msg = check_directory(directory, received_data)
        msg = pickle.dumps(msg)
        sock.send(msg)
        print(f"Response sent to {addr}")
    except Exception as e:
        print(f"Error processing client {addr}: {e}")
        sock.close() # КАРОЧЕ НЕ ЕБИ МОЗГА И СДЕЛАЙ НОРМАЛЬНУЮ РЕАЛИЗАЦИЮ ПРИНЯТИЯ ДАННЫХ ПОСЛЕ ЭТОГО ТЫ СПОКОЙНО БУДЕШЬ ЗАКРЫВАТЬ СОКЕТЫ И НАДЕЮСЬ КАРОЧ ЧТО В ЭТОМ БЕДА ДА


def create_directories(folder):
    if not os.path.isdir(os.path.join(os.getcwd(), folder)):
        os.mkdir(os.path.join(os.getcwd(), folder))


def check_directory(directory, dir_client):
    dir_server = os.listdir(directory)
    for f in dir_client:
        if f not in dir_server:
            print("Sending request to remove")
            return f"remove {f}"

    for f in dir_server:
        if f not in dir_client:
            print("Sending request to create")
            return File(f, directory)
    print("Sending OK response")
    return "OK"


class File:
    def __init__(self, name, directory):
        self.name = name
        self.directory = directory
        self.data = self.read_data()

    def read_data(self):
        with open(os.path.join(self.directory, self.name)) as f:
            return f.readlines()


srv = socket.socket(TYPE, PROTOCOL)
srv.bind((HOST, PORT))

create_directories(folder)
srv.listen(4)
while True:
    print("Listening on port 9090")
    sock, addr = srv.accept()
    print("Client connected:", addr)
    try:
        thread = threading.Thread(target=client_processing, args=(sock, addr))
        thread.start()
    except Exception as e:
        print("Error creating thread:", e)
