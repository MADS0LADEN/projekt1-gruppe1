import socket


def handle_client(client_socket):
   
    request = client_socket.recv(1024).decode('utf-8')
    
    print("Modtaget data fra klient:", request)
   
    form_data = request.split('\n')[-1]
    
    print("Formdata:", form_data)
    
    response = "HTTP/1.1 200 OK\n\nData modtaget: " + form_data
    client_socket.send(response.encode('utf-8'))
    
 
    client_socket.close()


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


server_socket.bind(('localhost', 8080))


server_socket.listen(1)
print('Serveren venter på forbindelse...')

while True:   
    client_socket, client_address = server_socket.accept()
    print('Forbundet til', client_address)
  
    handle_client(client_socket)
