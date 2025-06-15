import threading
import socket 
import argparse
import os
import sys
import tkinter as tk

class Send(threading.Thread):
    
    # listens for user input from cmd line

    #name:str ->  the username provided by the user