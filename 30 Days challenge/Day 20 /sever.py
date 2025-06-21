# import socket

# s = socket.socket()
# print("Socket successfully created ")

# port = 56789
# s.bind(('', port)) # Bind method takes two parameter IP and port, IP is empty here server 
# # Can listen to other Request from other network. 
# # For port it will return the port that is pre-define. 
# print(f'socket bind to port {port}')
# s.listen(5) # It has capability to listen 5 request. 
# print("Socket is listening ")

# while True:
#     c, addr = s.accept()
#     print("Got connection from", addr)
#     message = ("Thanks for connectioning")
#     c.send(message.encode())
#     c.close()
    
    
import socket

s = socket.socket()
print("Socket successfully created")

port = 56789
s.bind(('', port))
print(f'Socket bind to port {port}')

s.listen(5)
print("Socket is listening")

while True:
    c, addr = s.accept()
    print("Got connection from", addr)

    # Receive something from client (like telnet)
    data = c.recv(1024)
    print("Client says:", data.decode())

    # Send a response
    message = "Thanks for connecting"
    c.send(message.encode())

    c.close()
