#https://www.geeksforgeeks.org/how-to-get-file-size-in-python/
#https://stackoverflow.com/questions/33913308/socket-module-how-to-send-integer
# Taken from https://steelkiwi.com/blog/working-tcp-sockets/
import sys
from re import S
import socket
import os

#socket p.s if you want to not deal witht the VM just put something else in the connect
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((sys.argv[1], int(sys.argv[2])))
s.send("hello vietnam".encode("utf-8"))
U = "utf-8"



# the hub ask all needed questions
def ClientSock():
    # I have no idea why these do not read on the VM works in the local maching implemention even used the sys.argv and the .split() would not get value from the VN
    command = input("Enter command ")
    print(command)
    s.send(command.encode(U))
    filename = input("enter file")
    s.send(filename.encode(U))  
    if(command == "remap"):
        amount = (input("how much you want"))
        s.send(amount.encode(U))  

    if ("put" in command ):
        put(filename)
    elif("get" in command ):
        get(filename)
    elif("remap" in command ):
        remap(amount,filename)
    else:
        quit()


#put the stuff on the server
def put(fileName):

    File = open(fileName, "r")
    s.send(fileName.encode("utf-8"))
    file_size = os.path.getsize(fileName)
    s.send(str(file_size).encode("utf-8"))
    print(file_size)
    while True:
        read = File.read(1000)
        print(read)
        if (read == ''):
                print("break")
                break
        s.send(read.encode("utf-8"))

    File.close()
    ClientSock()

   

# gets the file from server
def get(name):
    print(name)
    s.send(name.encode("utf-8"))
    size = int(s.recv(1024).decode("utf-8"))
    print(size)
    File = open("newfile", "w")
    print(size)
    while True:
        print("hello bitch")
        size = size - 1000
        print("hello bitch2")
        amount = s.recv(1000).decode("utf-8")
        File.write(amount)
        if size < 0:
            break

    print("over here too")
    File.close()
    ClientSock()

# very simple just send the name of file and the amound
def remap(amount,name):
    s.send(name.encode("utf-8"))
    s.send(amount.encode("utf-8"))


def quit():
    s.send("quit".encode("utf-8"))
    print(s.recv(1024).decode("utf-8"))
    quit()


ClientSock()
