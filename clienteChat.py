#Usando Python3
#Cliente de Chat com interface Tkinter

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter

def receive():
    #Trata o recebimento de mensagens
    while True:
        try:
            #função recv() interrompe a execução até receber uma mensagem, após, a mensagem é anexa na msg_list
            msg = cliente_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except OSError: #Cliente pode ter deixado o chat
            break

def send(event=None): 
    """event está como argumento pois o Tkinter, quando o botão enviar é pressionado, passa o argumento implicitamente"""
    #Trata o envio de mensagens
    msg = my_msg.get() #my_msg e o campo de entrada na GUI
    my_msg.set("") #limpa a entrada
    cliente_socket.send(bytes(msg,"utf8"))
    if msg == "{sair}":
        cliente_socket.close() #fecha o socket do cliente se msg = sair
        top.quit() #fecha o app da GUI

def on_closing(event=None):#Essa função deve ser chamada quando a janela é fechada
    my_msg.set("{sair}")
    send()

####################################################################################################

#Início da GUI
top = tkinter.Tk()
top.title("Chat")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()
my_msg.set("Digite sua mensagem aqui...")
scrollbar = tkinter.Scrollbar(messages_frame) #Para rolar para mensagens anteriores

#Parte da GUI que contém as mensagens
msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack

messages_frame.pack()

campo_entrada = tkinter.Entry(top, textvariable=my_msg)
campo_entrada.bind("<Return>",send)
campo_entrada.pack()
send_button = tkinter.Button(top, text='Enviar', command=send)
send_button.pack()

"""Aqui executamos a função on_closing quando o usuário fechar a janela"""
top.protocol("WM_DELETE_WINDOW", on_closing)
#Fim da GUI
####################################################################################################

HOST = input('Digite o IP do Servidor: ')
PORT = int(input('Digite a porta para conexão(Porta Padrão 1997): '))

BUFSIZ = 4096
ADDR = (HOST, PORT)

cliente_socket = socket(AF_INET, SOCK_STREAM)
cliente_socket.connect(ADDR)

recebe_thread = Thread(target=receive)
recebe_thread.start() #Thread para o cliente receber mensagens
tkinter.mainloop() #Inicia execução da inteface