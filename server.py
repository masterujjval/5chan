import threading
import socket
import argparse
import sys
from cryptography.fernet import Fernet # type: ignore

class Server(threading.Thread):
    def __init__(self, host,port):
        super().__init__()
        self.connections=[]
        self.host=host
        self.port=port


    def run(self):
        sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        sock.bind((self.host, self.port))

        sock.listen(1)
        print("Listening at ", sock.getsockname())

        while True:
            # to accept new connections
            sc,sockname=sock.accept()
            print(f"New connection from {sc.getpeername()} to {sc.getsockname()}")

            # crate a new thread
            server_socket=ServerSocket(sc,sockname,self)

            # start a new thread
            
            server_socket.start()

            # Add thread to active connection 

            self.connections.append(server_socket)
            print("Ready to receive message from ", sc.getpeername())



    def broadcast(self, message, source):

        for connection in self.connections:

            # send to all connections client accept the source client

            if connection.sockname!=source:
                connection.send(message)


    def remove_connection(self,connection):
        self.connections.remove(connection)





class ServerSocket(threading.Thread):
    def __init__(self, sc, sockname, server):
        super().__init__()
        self.sc=sc
        self.sockname=sockname
        self.server=server
        self.alive = True 
        

    def run(self):

        while True:
            try:
        
                message=self.sc.recv(4096).decode("ascii")

                if message:
                    print(f"{self.sockname} sent a messsage")
                    self.server.broadcast(message,self.sockname)

                else:
                    print(f"{self.sockname} has closed the connection")
                    self.sc.close()
                    server.remove_connection(self)

                    return
            except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
                    print(f"{self.sockname} has closed the connection")
                    
                    self.server.broadcast("5chan: Anon left the chat",self.sockname)

                    self.sc.close()
                    server.remove_connection(self)
                    return

    def send(self,message):
        self.sc.sendall(message.encode("ascii"))
        

def exit(server):
    while True:
        ipt=input("")
        if ipt =="q":
            print("Closing all connections...")

            for connection in server.connections:
                connection.sc.close()


            print("Shutting down the server...")
            sys.exit(0)


if __name__=="__main__":
    parser=argparse.ArgumentParser(description="Anon Chat Server")
    host=input("Server address, anons! (No gay https:// or http://, just the good stuff. localhost if you're a true shut-in): ").strip().lower()
    host= host if host else "0.0.0.0"

    # generate key for secure chatting in the room

    key_option= input("Want a key for chat encryption? y/n: ").strip().lower()
    if key_option=='y':
        key_option=Fernet.generate_key()
        print(f"Yo, anons! Got a secret decoder ring for your degenerate chats. Key's here: \n\033[31m{key_option.decode('ascii')}\033[0m\n")

    else:
        key_option=None 


    # create and start server thread

    server=Server(host,1060)
    

    server.start()

    exit=threading.Thread(target=exit, args=(server,))

    exit.start()
