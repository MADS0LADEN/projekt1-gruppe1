import socket
from datetime import datetime

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Get local machine name
# Get the IP address of the local machine
host = "0.0.0.0"

port = 7913

# Bind to the port
server_socket.bind((host, port))
print("Connect to:", f"{host}:{port}")

# Queue up to 5 requests
server_socket.listen(5)

while True:
    # Establish a connection
    client_socket, addr = server_socket.accept()
    # print(f"Got a connection from {addr}")

    # Receive data from the client
    data = client_socket.recv(1024)
    received_msg = data.decode()

    # unpack = received_msg.replace(")", "").replace("(", "").replace(" ", "").split(",")
    unpack = [
        item
        for item in received_msg.replace(")", "")
        .replace("(", "")
        .replace(" ", "")
        .split(",")
        if item != ""
    ]

    log = f"{datetime.now()} {unpack}"
    print(log)
    # Write the received message to the log file
    with open("log.txt", "a") as log_file:
        log_file.write(log + "\n")

    # Close the connection
    client_socket.close()
