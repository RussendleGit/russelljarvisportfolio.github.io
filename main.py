import socket

SERVER_HOST = "0.0.0.0" #any IP can see this, if 0.0.0.1 only I can see this
SERVER_PORT = 8024 #it is hosted on port 8024. starts with 80 because of convention with HTTP because HTTP is hosted on 80

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # 1 on 0 off
server_socket.setblocking(True) # False for never blocking execution of code. True if so

server_socket.bind((SERVER_HOST, SERVER_PORT)) #any IP can see this, and it is hosted on port 8024

server_socket.listen(5) # number of connections that can be accessed

print(f"listening on port {SERVER_PORT} ...")

"""
#THIS WILL ONLY LISTEN TO ONE CONNECTION
while True:
    try: # try seeing if user is connecting
        client_socket, client_address = server_socket.accept() 
        print(client_socket); print(client_address)
    except: # if not wait a second
        print("Error connecting to client. Retrying ...")
        time.sleep(1)
        continue
"""

while True:
    client_socket, client_address = server_socket.accept() 
    request = client_socket.recv(1024).decode() # max packet size. and decode it into human readable
    print(request)
    
    headers = request.split("\n")
    first_header_components = headers[0].split()
    
    http_method = first_header_components[0]
    path = first_header_components[1]
    if http_method == 'GET':
        try:
            if path == '/':
                file_input = open('index.html')
            elif path == '/cybersecurity':
                file_input = open('cybersecurity.html')
            content = file_input.read()
            file_input.close()
            response = 'HTTP/1.1 200 OK\n\n' + content
        except ValueError:
            print("failed to load recourses")
    else:
        response = 'HTTP/1.1 405 Method Not Allowed\n\nAllow: GET'
        
    client_socket.sendall(response.encode())
    client_socket.close()