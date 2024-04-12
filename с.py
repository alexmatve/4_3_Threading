import socket
import os
import pickle
import time


class File:
    def __init__(self, name, directory):
        self.name = name
        self.directory = directory
        self.data = self.read_data()

    def read_data(self):
        with open(os.path.join(self.directory, self.name)) as f:
            return f.readlines()

SERVER = "localhost"
PORT = 9090

TYPE = socket.AF_INET
PROTOCOL = socket.SOCK_STREAM

folder = "f_1"
directory = os.path.join(os.getcwd(), folder)


def create_directories(folder):
    if not os.path.isdir(os.path.join(os.getcwd(), folder)):
        os.mkdir(os.path.join(os.getcwd(), folder))


def take_info(directory):
    info = os.listdir(directory)
    return info


def create_file(data, directory):
    with open(os.path.join(directory, data.name), "w") as f:
        for line in data.data:
            f.write(line)
        print(f"File {data.name} created")


def remove_file(msg, directory):
    name = msg[len('remove') + 1:]
    os.remove(os.path.join(directory, name))
    print(f"File {name} removed")


def change_dirs(data, directory):
    if data == "OK":
        print("Received OK response")
        return
    if isinstance(data, str):
        remove_file(data, directory)
        print("File removed")
    else:
        create_file(data, directory)


create_directories(folder)

while True:
    try:
        sock = socket.socket(TYPE, PROTOCOL)
        sock.connect((SERVER, PORT))
        msg = take_info(directory)
        msg = pickle.dumps(msg)
        sock.send(msg)

        print("Directory state sent to server")

        received_data = b''
        fl = False
        while True:
            if fl:
                sock.settimeout(2.0)
                try:
                    print("kjflajfkal")
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

        if received_data:
            received_data = pickle.loads(received_data)
            print("Response received from server")
            change_dirs(received_data, directory)
    except Exception as e:
        print("Error:", e)
    finally:
        print("Closing connection.")
        sock.close()
        time.sleep(15)  # Wait for next synchronization
