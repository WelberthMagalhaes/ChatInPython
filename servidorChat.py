#Usando Python3
#Servidor de Chat.
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s está conectado." % client_address)
        client.send(bytes("Digite seu nome e pressione enter.", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""
    try:
        name = client.recv(BUFSIZ).decode("utf8")
        welcome = 'Bem Vindo(a) %s! Se quiser sair digite {sair}.' % name
        client.send(bytes(welcome, "utf8"))
        msg = "%s entrou no chat" % name
        broadcast(bytes(msg, "utf8"))
        clients[client] = name

        while True:
            msg = client.recv(BUFSIZ)
            if msg != bytes("{sair}", "utf8"):
                broadcast(msg, name+": ")
            else:
                client.send(bytes("{sair}", "utf8"))
                print('test')
                client.close()
                print('test2')
                del clients[client]
                broadcast(bytes("%s saiu do chat." % name, "utf8"))
                break
    except:
        print("%s saiu do chat" % name)


def broadcast(msg, prefix=""):  # prefix is for name identification.
  #Envia a mensagem para todos os clientes.
  
    for sock in clients:
      sock.send(bytes(prefix, "utf8")+msg)

        
clients = {}
addresses = {}

HOST = ''
PORT = 1997
BUFSIZ = 4096
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()