import socket

# Server details
server_ip = "127.0.0.1"  # Replace with the actual server IP address
server_port = 7913  # Replace with the actual server port

# Create a TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((server_ip, server_port))

# Send data to the server
data = "ALARM\nLækage i kølerummet!"
client_socket.send(data.encode())

# Receive data from the server
received_data = client_socket.recv(1024).decode()
print("Received:", received_data)

# Close the connection
client_socket.close()
