
import socket
import threading

HOST = "127.0.0.1"
PORT = 5000

pseudo = input("Entre ton pseudonyme : ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connexion au serveur
try:
    client.connect((HOST, PORT))
    print("Connecté à MNS Chat !")
except OSError:
    print("Erreur : impossible de joindre le serveur.")
    client.close()
    exit()

# Recevoir les messages
def receive():
    try:
        while True:
            message = client.recv(4096)

            if not message:
                print("\nLe serveur est déconnecté.")
                break

            print("\n" + message.decode("utf-8"))

    except OSError:
        print("\nConnexion interrompue.")

# Recevoir les messages en arrière-plan
thread = threading.Thread(target=receive, daemon=True)
thread.start()

# Envoyer les messages
try:
    while True:
        message = input()

        if message == "/quit":
            break

        if message.strip():
            client.sendall(
                f"{pseudo} : {message}\n".encode("utf-8")
            )

except OSError:
    print("Erreur de connexion.")

finally:
    client.close()
