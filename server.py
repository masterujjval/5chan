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
            

            # crate a new thread
            server_socket=ServerSocket(sc,sockname,self)

            # start a new thread
            
            server_socket.start()

            # Add thread to active connection 

            self.connections.append(server_socket) # \033[32m green \033[31m red \033[0m reset
            print(f"New connection from {sc.getpeername()} to {sc.getsockname()}. Anons online: {len(self.connections)}")
            self.broadcast(f"\033[32m5chan: Anon joined the chat. Anons online: {len(self.connections)}", sockname)
            print("Ready to receive message from ", sc.getpeername())
            sc.sendall(f"Anons online: {len(self.connections)}".encode("ascii"))




    def broadcast(self, message, source):
        dead_connections = []
        for connection in self.connections:
            if connection.sockname != source:
                try:
                    connection.send(message)
                except (BrokenPipeError, ConnectionAbortedError, ConnectionRefusedError, ConnectionResetError):
                    dead_connections.append(connection)

    # Clean up disconnected clients
        for dead in dead_connections:
            print(f"[!] Removing dead connection: {dead.sockname}")
            self.connections.remove(dead)





    def remove_connection(self,connection):
        self.connections.remove(connection)





class ServerSocket(threading.Thread):
    def __init__(self, sc, sockname, server):
        try:
            super().__init__()
            self.sc=sc
            self.sockname=sockname
            self.server=server
            self.alive = True 
        except ConnectionResetError:
            print("Anon left the server")
        

    def run(self):

        while True:
            try:
        
                message=self.sc.recv(4096).decode("ascii")

                if message:
                    print(f"{self.sockname} sent a messsage")
                    self.server.broadcast(message,self.sockname)

                else:
                    
                    self.server.broadcast(f"\033[31m5chan: Anon left the chat. Anons online: {len(self.server.connections)-1}",self.sockname)
                    self.sc.close()
                    server.remove_connection(self)
                    print(f"{self.sockname} has closed the connection. Anons online: {len(self.server.connections)}")

                    return
            except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError , ConnectionRefusedError):
                    
                    self.server.broadcast(f"\033[31m5chan: Anon left the chat.Anons online: {len(self.server.connections)-1}",self.sockname)

                    self.sc.close()
                    server.remove_connection(self)
                    print(f"{self.sockname} has closed the connection. Anons online: {len(self.server.connections)}")
                    return
    
    # send message to the client
    def send(self, message):
        try:
            self.sc.sendall(message.encode("ascii"))
        except Exception as e:
            print(f"[!] Send failed to {self.sockname}: {e}")
            raise
        

def exit(server):
    while True:
        try:
            ipt=input("")
            if ipt =="q":
                print("Closing all connections...")

                for connection in server.connections:
                    connection.sc.close()


                print("Shutting down the server...")
                sys.exit(0)
        except Exception:
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
