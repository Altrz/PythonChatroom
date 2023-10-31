#this file is used to start and run the server. People can run the client program to acess this server


#modules needed to run the server 
import socket 
import select 
import sys 
from _thread import *

#line 12 establishes our server as a variable. "AF_Inet" is the adress of the socket and "SOCK_STREAM" indicates that it will -
# - constantly reupdate
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# checks to see if computer is providing all requirements and quits if it doesnt
if len(sys.argv) != 3: 
    print ("Correct usage: script, IP address, port number")
    exit()


#Establishes Identifiers for the system
IP_address = str(sys.argv[1]) 
Port = int(sys.argv[2])
#note the variable types (int & str) and that sys.argv[0] is already taken by the server script

#binds the server to an entered IP address and at the specified port number. The client script must use the same port and ip in order to connect
server.bind((IP_address, Port)) 

#number of connections the server listens to
server.listen(10)

#establishes a list of users accesing server
list_of_clients = []


#what happens when a user joins server
def clientthread (connection, address):
    connection.send("welcome to the chatrrom")

    while True:
        try:
            message = connection.receive(2048)
            
            if message:
                #prints the address of sender + the message in the server terminal (notice type of brackets)
                print ("(" + address[0] + ") " + message) 
                # Calls broadcast function to send message to everyone accessing server 
                message_to_send = "<" + address[0] + "> " + message 
                broadcast(message_to_send, connection) 

            else:
                #no message or error so it breaks the connection by using remove function
                remove(connection)
        
        except:
            continue

#broadcast function used to send to other clients
def broadcast(message, connection): 
    for clients in list_of_clients: 
        if clients!=connection: 
            try: 
                clients.send(message) 
            except: 
                clients.close() 
                # if the link is broken, we remove the client 
                remove(clients)

#remove function. used to remove unwanted connections
def remove(connection): 
    if connection in list_of_clients: 
        list_of_clients.remove(connection)

while True: 
 
    """Accepts a connection request and stores two parameters, 
    conn which is a socket object for that user, and addr 
    which contains the IP address of the client that just 
    connected"""
    conn, addr = server.accept() 
 
    """Maintains a list of clients for ease of broadcasting 
    a message to all available people in the chatroom"""
    list_of_clients.append(conn) 
 
    # prints the address of the user that just connected 
    print (addr[0] + " connected")
 
    # creates and individual thread for every user 
    # that connects 
    start_new_thread(clientthread,(conn,addr))     
 
conn.close() 
server.close() 
