# https://stackoverflow.com/questions/27893804/udp-client-server-socket-in-python
# https://pythontic.com/modules/socket/udp-client-server-example
# https://stackoverflow.com/questions/15909064/python-implementation-for-stop-and-wait-algorithm
# https://stackoverflow.com/questions/17667903/python-socket-receive-large-amount-of-data

import socket
import os
import sys
#socket with UDP
conn = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
conn.bind(('', int(sys.argv[1])))
conn.settimeout(500)
U = "utf-8"
ack = True
while ack:
        try:
            receive, adress = conn.recvfrom(1000)
            conn.sendto("FIN".encode(U),adress)
            ack = False
            print(receive,adress)
        except socket.timeout:
            print("your out of luck server ain't fix #1")
            break

# Taken from https://steelkiwi.com/blog/working-tcp-sockets/

# hub for the socket
def ServerSock():
    ack = True
    File = ""
    while ack:
        try:
            receive, adress = conn.recvfrom(1000)
            conn.sendto("FIN".encode(U),adress)
            ack = False
        except socket.timeout:
            print("your out of luck server ain't fix #2")
            break
    receive = receive.decode(U)
    ack = True
    while ack:
        try:
            File, adress = conn.recvfrom(1000)
            File = File.decode(U)
            conn.sendto("FIN".encode(U),adress)
            ack = False
            print(File)
        except socket.timeout:
            print("your out of luck server ain't fix #3 ")
            break
        
    print(receive)
    if ("put" in receive):
        put(File)
    elif("get" in receive):
        get(File)
    elif("remap" in receive):
        remap(File)
    elif("quit" in receive):
        quit()



# gets the info from the server side
def put(FileName):
    ack = True
    size = ""
    size2 = 0
    amount = ""
    File = open("newfile", "w")
    while ack:
        try:
            size, adress = conn.recvfrom(1000)
            size2 = int(size)
            conn.sendto("FIN".encode(U),adress)
            ack = False
        except socket.timeout:
            print("your out of luck server ain't fix #5")
            break
    print(size)
    while True:
        size2 = size2 - 1000
        try:
            amount, adress = conn.recvfrom(1000)
            conn.sendto("FIN".encode(U),adress)
        except socket.timeout:
            print("your out of luck server ain't fix #6")
            break
        File.write(amount.decode(U))
        if size2 < 0:
            break

    print("over here too")
    File.close()
    ServerSock()

#sends the info to the client
def get(fileName):
    print("hello from serv")
    File = open(fileName, "r")
    file_size = os.path.getsize(fileName)
    print(file_size , "I am file size")
    ack = ""
    print("here server")
    while ack != "FIN":
        try:
            
            conn.sendto(str(file_size).encode(U), adress)
            ack, address = conn.recvfrom(1000)
            ack = ack.decode(U)
            print(ack + "here lies ack")
        except socket.timeout:
            print("your out of luck server ain't fix")
    while True:
        read = File.read(1000)
        print(read)
        if (read == ''):
            print("break")
            break
        try:
            conn.sendto(read.encode(U), adress)
            ack, address = conn.recvfrom(1000)
            if(ack.decode(U) == "FIN"):
                continue

        except socket.timeout:
            print("your out of luck server ain't fix")

    File.close()
    ServerSock()

# https://www.geeksforgeeks.org/python-program-to-read-character-by-character-from-a-file/ the code for reading letter by letter

# more comprehensive but takes lettter by letter converts to asckII and adds the amount then goes and rights the new letter in a new file
def remap(fileName):
    size = ""
    size2 = 0
    ack = True
    file = open(fileName, 'r')
    while ack:
        try:
            size, adress = conn.recvfrom(1000)
            size2 = int(size)
            print(size, 'hewwo my name is size pls be gentle with me senpai')
            conn.sendto("FIN".encode(U),adress)
            ack = False
        except socket.timeout:
            print("your out of luck server ain't fix #5")
            break
    newname = "remap_" + fileName
    newfile = open(newname, 'w')
    while 1:

        # read by character
        char = file.read(1)
        if not char or ord(char) == 0:
            break
        x = chr(ord(char) +  size2)
        newfile.write(x)
        

    file.close()
    newfile.close()
    ServerSock()

#quits the program
def quit():
    ack = True
    receive = ""
    while ack:
        try:
            receive, adress = conn.recvfrom(1000)
            conn.sendto("FIN".encode(U),adress)
            ack = False
            receive = receive.decode(U)
        except socket.timeout:
            print("your out of luck server ain't fix #2")
            break   
        if(receive == "quit"): 
            quit()



ServerSock()
