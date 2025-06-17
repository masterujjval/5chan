import threading
import socket 
import sys
import random
from cryptography.fernet import Fernet #type:ignore
"""
NOTE: if you are already having running server or shared room server and port change the port number and 
connect using that server address not need to run \'server.py\' for that.

Type "QUIT" to leave the room
"""

global key

class Send(threading.Thread):
    
    # listens for user input from cmd line

    #name:str ->  the username provided by the user
    

    def __init__(self,sock,name):
        super().__init__()

        self.sock=sock
        self.name=name

    def run(self):
        # listens for user input from cmd line
        # type "Quit" to close the connection

        while True:
            try:
                print('{}: '.format(self.name),end='')
                sys.stdout.flush()
                message=sys.stdin.readline()[:-1]

                if message == "QUIT":
                    self.sock.sendall('\n\033[31m5chan : {} has left the chat.\033[0m'.format(self.name).encode("ascii"))
                    break

                if key:
                    fernat = Fernet(key)
                    encrypted = fernat.encrypt(message.encode())
                    final_message=b"[ENC]"+encrypted
                    self.sock.sendall('{}:'.format(self.name).encode("utf-8") + final_message)

                else:
                    self.sock.sendall('{}: {}'.format(self.name, message).encode("utf-8"))
                # send message to server for broadcasting
                
                # else:
                #     self.sock.sendall('{}: {}'.format(self.name, message).encode("ascii"))

            except OSError:
                return

        print("\nQuitting...")
        self.sock.close()
        sys.exit(0)


# to receieve messages
class Receive(threading.Thread):

    #Listens for incoming messages

    def __init__(self,sock,name):
        super().__init__()

        self.name=name
        self.sock=sock
        self.messages=None

    def run(self):
        while True:
            try:
                message = self.sock.recv(4096)

                if not message:
                    print('\nConnection closed by 5chan.')
                    self.sock.close()
                    sys.exit(0)

                try:
                    message_str = message.decode()

                    if "[ENC]" in message_str:
                        name, enc_msg = message_str.split(":", 1)
                        enc_msg = enc_msg.strip()

                        if enc_msg.startswith("[ENC]") and key:
                            enc_bytes = enc_msg[5:].encode()
                            fernet = Fernet(key)
                            decrypted = fernet.decrypt(enc_bytes).decode()
                            message_str = f"{name}: {decrypted}"
                        elif not key:
                            message_str = f"{name}: You need private key to view this message"
                            print(f'\r{message_str}\n{self.name}: ', end='', flush=True)
                            continue

                    print(f'\r{message_str}\n{self.name}: ', end='', flush=True)

                except Exception as e:
                    print(f"[!] Error handling message: {e}")
                    continue
            
            except (ConnectionAbortedError):
                print("Anon closed the call...")
                self.sock.close()
                sys.exit(0)
            except (ConnectionResetError):
                print("\n5chan server closed...")
                self.sock.close()
                sys.exit(0)



            


class Client:
    # management of client server connection 
    def __init__(self, host,port):
        self.host=host
        self.port=port
        self.sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.name=None

        self.messages=None

    def start(self):
        print("Trying to connect to {}:{}...".format(self.host, self.port))
        self.sock.connect((self.host, self.port))

        print("Successfully connected to {}:{}".format(self.host, self.port))

        print()

        self.name=input("Enter your username: ")

        
        #adding color
        ansi_colors = ["\033[30m", "\033[31m", "\033[32m", "\033[33m", "\033[34m", "\033[35m", "\033[36m", "\033[37m", "\033[90m", "\033[91m", "\033[92m", "\033[93m", "\033[94m", "\033[95m", "\033[96m", "\033[97m"]
        rand=random.randint(0,len(ansi_colors)-1)
        
        self.name=ansi_colors[rand]+self.name+"\033[0m"


        print()

        print("Welcome {}! Welcome to 5chan CLI messaging community!".format(self.name))

        # create send and receive threads

        send=Send(self.sock,self.name)
        receive=Receive(self.sock, self.name)

        # starting the threads
        send.start()
        receive.start()

        self.sock.sendall("\033[31m5chan: {} has joined the chat\033[0m".format(self.name).encode("ascii"))

        return receive
    

    def send(self, textInput):

        # sends msg 
        message=textInput.get()
        
        self.messages.insert(0, '{}: {} '.format(self.name, message))

        # TYPE QUIT to leave the chatroom 
        try:
            if message=="QUIT":
                self.sock.sendall('5chan: {} has left the chatroom '.format(self.name).encode("ascii"))
                print("\nQutting..")
                self.sock.close()
                sys.exit(0)

            # send message to the server for broadcasting
            else:
                self.sock.sendall("{}: {}".format(self.name,message).encode("ascii"))
        
        except (KeyboardInterrupt, ConnectionAbortedError):
            print("\nQutting...")
            self.sock.close()
            sys.exit(0)
            



def main(host, port):
    # initilize and run the gui app

    client=Client(host,port)
    receive=client.start()


if __name__=="__main__":
    host=input("Enter the server host address (without https:// or http://): ").strip().lower()
    port=input("Enter the server port number (default 1060): ").strip()
    port = port if port else 1060

    key=input("Do you have private key? y/n: ").strip().lower()
    if key=="y":
        key=input("Enter the private key: ").strip().lower()
        key=key.encode()

    else :
        key=None

    main(host, port)

