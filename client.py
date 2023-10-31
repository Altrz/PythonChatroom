# this file is run by each client accessing the server as a thread
#for comments on code up to line 14, see server.py

import socket 
import select 
import sys 
 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
if len(sys.argv) != 3: 
    print ("Correct usage: script, IP address, port number")
    exit() 
IP_address = str(sys.argv[1]) 
Port = int(sys.argv[2]) 
server.connect((IP_address, Port))

while True:
    # maintains a list of possible input streams 
    sockets_list = [sys.stdin, server]

    read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])
    
    #determines if the message is from you or not from each source connected to the server and formats accordingly
    for socks in read_sockets: 
        if socks == server: 
            message = socks.recv(2048) 
            print (message) 
        else: 
            message = sys.stdin.readline() 
            server.send(message) 
            sys.stdout.write("<You>") 
            sys.stdout.write(message) 
            sys.stdout.flush() 
server.close() 