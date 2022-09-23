# https://www.geeksforgeeks.org/python-program-to-read-character-by-character-from-a-file/ the code for reading letter by letter
# https://stackoverflow.com/questions/17667903/python-socket-receive-large-amount-of-data
# Taken from https://steelkiwi.com/blog/working-tcp-sockets/
import socket
import sys
import os
#server side of the socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(sys.argv[1])
s.bind(('', int(sys.argv[1])))
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.listen(5)
conn, addr = s.accept()
message = conn.recv(1024).decode("utf-8")
print(message)
U = "utf-8"

# the hub area recieves all there needs to make the magic
def ServerSock():
    amount = 0
    command = conn.recv(1000).decode(U)
    filename = conn.recv(1000).decode(U)
    if(command == "remap"):
        amount = int(conn.recv(1000).decode(U))
    if ("put" in command):
        put(filename)
    elif("get" in command):
        get(filename)
    elif("remap" in command):
        remap(amount,filename)
    else:
        quit()

    print("server")

#recieves the info and makes a newfile and puts the new information there
def put(fileName):
    File = open(fileName, "w")
    size = int(conn.recv(1024).decode("utf-8"))
    print(size)
    while True:
        size = size - 1000
        amount = conn.recv(1000).decode("utf-8")
        File.write(amount)
        if size < 0:
            break

    print("over here too")
    File.close()
    ServerSock()

# sends the info right back to the client
def get(fileName):
    File = open(fileName, "r")
    file_size = os.path.getsize(fileName)
    print(file_size)
    conn.send(str(file_size).encode("utf-8"))
    print(file_size)
    while True:
        read = File.read(1000)
        if (read == ''):
                print("break")
                break
        conn.send(read.encode("utf-8"))

    File.close()
    ServerSock()



# more comprehensive but takes lettter by letter converts to asckII and adds the amount then goes and rights the new letter in a new file
def remap(amount,fileName):

    file = open(fileName, 'r')
    newname = "remap_" + fileName
    newfile = open(newname, 'w')
    while 1:

        # read by character
        char = file.read(1)
        x = chr(ord(char) + amount)
        newfile.write(x)
        if not char:
            break

    file.close()
    newfile.close()
    ServerSock()

#quits program
def quit():
    conn.send("quit".encode("utf-8"))
    quit()
    print(conn.recv(1024).decode("utf-8"))



ServerSock()
