#Usando Python3
#Servidor de Chat.
#Trabalho Prático disciplina Fundamentos de Redes de Computadores
#Professor Marlon Paolo Lima

#Aluno Welberth Heider Magalhães de Araújo - 16.1.8111

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

def aceitar_conexoes_entrada():
    """Tratamento inicial da conexão do cliente"""
    while True:
    	#Retorna o novo objeto socket e o endereço na outra extremidade(conn, address)
        client, client_address = SERVER.accept()
        print("%s:%s está conectado." % client_address)
        #Envia 1ª mensagem pelo socket
        client.send(bytes("Digite seu nome e pressione enter.", "utf8"))
        addresses[client] = client_address
        Thread(target=controla_cliente, args=(client,)).start()


def controla_cliente(client):  # Recebe o socket de cliente
    """Controla uma conexão do cliente."""
    name = client.recv(BUFSIZ).decode("utf8") #Recebe o nome que o usuário digitar
    welcome = 'Bem Vindo(a) %s! Se quiser sair digite {sair}.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s entrou no chat" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name

    while True:
    	#recebe mensagem do cliente e envia à todos os conectados
        msg = client.recv(BUFSIZ)
        if msg != bytes("{sair}", "utf8"):
            broadcast(msg, name+": ")
        else:
            client.close()
            del clients[client]
            broadcast(bytes("%s saiu do chat." % name, "utf8"))
            print("%s saiu do chat" % name)
            break
    


def broadcast(msg, prefix=""):
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
    print("Esperando por conexões...")
    ACCEPT_THREAD = Thread(target=aceitar_conexoes_entrada)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
