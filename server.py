
import socket
import threading

HOST = "0.0.0.0"
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()

clients = []
lock = threading.Lock()

print(f"Serveur MNS Chat démarré sur le port {PORT}")

# Transmettre les messages aux autres clients
def broadcast(message, sender):
    with lock:
        connected = clients.copy()

    for client in connected:
        if client != sender:
            try:
                client.sendall(message)
            except OSError:
                pass

# Gérer chaque utilisateur
def handle_client(client):
    try:
        while True:
            message = client.recv(4096)

            if not message:
                break

            broadcast(message, client)

    except OSError:
        pass

    finally:
        with lock:
            clients.remove(client)

        client.close()
        print("Un utilisateur s'est déconnecté.")

# Accepter les nouvelles connexions
while True:
    client, address = server.accept()

    print(f"Nouvelle connexion : {address}")

    with lock:
        clients.append(client)

    thread = threading.Thread(
        target=handle_client,
        args=(client,),
        daemon=True
    )
    thread.start()
