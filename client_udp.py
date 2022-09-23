# https://stackoverflow.com/questions/27893804/udp-client-server-socket-in-python
# https://pythontic.com/modules/socket/udp-client-server-example
# https://stackoverflow.com/questions/15909064/python-implementation-for-stop-and-wait-algorithm
# https://www.geeksforgeeks.org/how-to-get-file-size-in-python/
# https://stackoverflow.com/questions/33913308/socket-module-how-to-send-integer
import socket
import os
import sys
#socket for the client side
U = "utf-8"
s = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
add1 = sys.argv[1]
add2 = int(sys.argv[2])
s.sendto("hello vietnam".encode(U), (add1, add2))
s.settimeout(500)

#hub for all inputs
def ClientSock():

    ClientInput = input("Enter command ")

    ack = ""
    while ack != "FIN":
        try:
            s.sendto(ClientInput.encode(U), (add1, add2))
            ack, address = s.recvfrom(1000)
            ack = ack.decode(U)
        except socket.timeout:
            print("your out of luck server ain't fix")
    NameFile = input("enter the File ")
    ack = ""
    while ack != "FIN":
        try:
            s.sendto(NameFile.encode(U), (add1, add2))
            print(NameFile + "I am file in clisock")
            ack, address = s.recvfrom(1000)
            ack = ack.decode(U)
        except socket.timeout:
            print("your out of luck server ain't fix")
    if ("put" in ClientInput):
        put(NameFile)
    elif("get" in ClientInput):
        get(NameFile)
    elif("remap" in ClientInput):
        remap(NameFile)
    elif("quit" in ClientInput):
        quit()



#sends the info to the server
def put(fileName):

    File = open(fileName, "r")
    file_size = os.path.getsize(fileName)
    ack = ""
    while ack != "FIN":
        try:
            s.sendto(str(file_size).encode(U), (add1, add2))
            ack, address = s.recvfrom(1000)
            ack = ack.decode(U)
        except socket.timeout:
            print("your out of luck server ain't fix")
    while True:
        read = File.read(1000)
        print(read)
        if (read == ''):
            print("break")
            break
        try:
            s.sendto(read.encode(U), (add1, add2))
            ack, address = s.recvfrom(1000)
            if(ack.decode(U) == "FIN"):
                continue

        except socket.timeout:
            print("your out of luck server ain't fix")

    File.close()
    ClientSock()

#recieves the info from the server
def get(fileName):
    ack = True
    acks = ""
    size = ""
    size2 = 0
    amount = ""
    File = open(fileName, "w")
    while acks != "FIN":
        try:
            acks, address = s.recvfrom(1000)
            print(acks)
            acks = acks.decode(U)
        except socket.timeout:
            print("your out of luck server ain't fix")
    while ack:
        try:
            size, adress = s.recvfrom(1000)
            size2 = int(size)
            print(size, 'hewwo my name is size pls be gentle with me senpai')
            s.sendto("FIN".encode(U), adress)
            ack = False
        except socket.timeout:
            print("your out of luck server ain't fix #5")
            break
    print(size)
    while True:
        size2 = size2 - 1000
        try:
            amount, adress = s.recvfrom(1000)
            s.sendto("FIN".encode(U), adress)
        except socket.timeout:
            print("your out of luck server ain't fix #6")
            break
        File.write(amount.decode(U))
        if size2 < 0:
            break

    print("over here too")
    File.close()
    ClientSock()

#sends the info for remmapoing
def remap(name):
    ack = ""
    amount = input("enter the amount you want to input ")
    while ack != "FIN":
        try:
            s.sendto(amount.encode(U), (add1, add2))
            ack, address = s.recvfrom(1000)
            ack = ack.decode(U)
        except socket.timeout:
            print("your out of luck server ain't fix")
            
    print(s.recv(1024).decode(U))
    ClientSock()

#quits the program
def quit():
    ack = ""
    while ack != "FIN":
        try:
            s.sendto("quit".encode(U), (add1, add2))
            ack, address = s.recvfrom(1000)
            ack = ack.decode(U)
        except socket.timeout:
            print("your out of luck server ain't fix")
    print(s.recv(1024).decode(U))


ClientSock()
