import threading
import socket

host = '127.0.0.1'
port = 59000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
aliases = []

# Broadcast message to all connected clients
def broadcast(message):
    for client in clients:
        try:
            client.send(message)
        except:
            pass  # In production, log this properly

# Handle messages from a single client
def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            alias = aliases[index]
            broadcast(f"{alias.decode('utf-8')} has left the chat room!".encode('utf-8'))
            aliases.remove(alias)
            break

# Accept new clients
def receive():
    while True:
        print("Server is running and listening ..... ")
        client, addr = server.accept()
        print(f"Connection is established with {str(addr)}")

        client.send('alias?'.encode('utf-8'))
        alias = client.recv(1024)
        aliases.append(alias)
        clients.append(client)

        print(f"The alias of the client is {alias.decode('utf-8')}")
        broadcast(f'{alias.decode("utf-8")} has connected to the chat room.'.encode('utf-8'))
        client.send("You are now connected".encode('utf-8'))

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()


if __name__ == "__main__":
    receive()
