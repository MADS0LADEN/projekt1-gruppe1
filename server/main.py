import smtplib
import socket

# TCP server configuration
HOST = "localhost"
PORT = 7913

# Email configuration
SMTP_SERVER = "smtp.example.com"
SMTP_PORT = 587
SENDER_EMAIL = "sender@example.com"
SENDER_PASSWORD = "password"
RECIPIENT_EMAIL = "recipient@example.com"


def send_email(subject, message):
    server = None
    try:
        # Connect to the SMTP server
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)

        # Compose the email
        email = f"Subject: {subject}\n\n{message}"

        # Send the email
        server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, email)
        print("Email sent successfully!")

    except Exception as e:
        print(f"An error occurred while sending the email: {e}")

    finally:
        # Disconnect from the SMTP server
        server.quit()


def handle_request(client_socket):
    # Receive data from the client
    data = client_socket.recv(1024).decode()

    # Process the request
    subject, message = data.split("\n", 1)
    # send_email(subject, message)
    print(subject, message)

    # Send response to the client
    response = "Email sent successfully!"
    client_socket.send(response.encode())

    # Close the client socket
    client_socket.close()


def start_server():
    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific address and port
    server_socket.bind((HOST, PORT))

    # Listen for incoming connections
    server_socket.listen()

    print(f"Server listening on {HOST}:{PORT}")

    while True:
        # Accept a client connection
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address[0]}:{client_address[1]}")

        # Handle the client request
        handle_request(client_socket)


start_server()
