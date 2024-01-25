import socket


def send_tcp_packet(ip, port):
    # Create a TCP socket

    try:
        while True:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip, port))
            # Send data
            data = input("Enter the data to send (or 'q' to quit): ")
            if data == "q":
                break
            sock.sendall(data.encode())
            sock.close()

    except Exception as e:
        print("Error:", str(e))

    finally:
        # Close the socket
        sock.close()


# Example usage
ip = input("Enter the IP address: ")
port = 7913

send_tcp_packet(ip, port)
