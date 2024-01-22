import socket
import time

from sensor import *


def log():
    return Sensor().read(), Sensor().diff()


def send(*msg):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "79.171.148.171"
    port = 7913
    try:
        s.connect((host, port))
        s.send(str(msg).encode())
        # print(msg)
    except Exception:
        pass
    finally:
        s.close()


# if __name__ is "__main__":
if True:
    while True:
        send(log())
        time.sleep(1)
