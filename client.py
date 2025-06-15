import threading
import socket 
import argparse
import os
import sys

"""
NOTE: if you are already having running server or shared room server and port change the port number and 
connect using that server address not need to run \'server.py\' for that.

Type "QUIT" to leave the room
"""

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
            print('{}: '.format(self.name),end='')
            sys.stdout.flush()
            message=sys.stdin.readline()[:-1]

            if message=="QUIT":
                self.sock.sendall('Server : {} has left the chat.'.format(self.name).encode("ascii"))
                break


            # send message to server for broadcasting
            
            else:
                self.sock.sendall('{}: {}'.format(self.name, message).encode("ascii"))

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
        #Recieves data from the server and displays it in the gui

        while True:
            message=self.sock.recv(1024).decode("ascii")

            if message:
                if self.messages:
                    self.messages.insert(0, message)
                    print("hi")
                    print('\r{}\n{}: '.format(message, self.name), end='')

                else:
                    print('\r{}\n{}: '.format(message, self.name), end='')



            else:
                print('\n No. We have lost connection to the server!')
                print('\nQuitting...')

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

        self.name=input("Enter your name: ")

        print()

        print(" Welcome {}! Welcome to Node Chat CLI messaging community!".format(self.name))

        # create send and receive threads

        send=Send(self.sock,self.name)
        receive=Receive(self.sock, self.name)

        # starting the threads
        send.start()
        receive.start()

        self.sock.sendall("Server: {} has joined the chat. say hi".format(self.name).encode("ascii"))

        return receive
    

    def send(self, textInput):

        # sends msg from textInput form gui
        message=textInput.get()
        textInput.delete(0,tk.END)
        self.messages.insert(tk.END, '{}: {} '.format(self.name, message))

        # TYPE QUIT to leave the chatroom 
        if message=="QUIT":
            self.sock.sendall('Server: {} has left the chatroom '.format(self.name).encode("ascii"))
            print("\nQutting..")
            self.sock.close()
            sys.exit(0)

        # send message to the server for broadcasting
        else:
            self.sock.sendall("{}: {}".format(self.name,message).encode("ascii"))


def main(host, port):
    # initilize and run the gui app

    client=Client(host,port)
    receive=client.start()


if __name__=="__main__":
    parser=argparse.ArgumentParser(description="Chatroom Server")
    parser.add_argument("host",help="Interface the server listens at")
    parser.add_argument("-p",metavar="PORT",type=int, default=1060, help="TCP port (default 1060)")

    args=parser.parse_args()

    main(args.host, args.p)

