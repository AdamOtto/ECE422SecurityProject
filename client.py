"""
References:
    https://pymotw.com/2/SocketServer/
"""
import logging
import sys
import socket
import os

#Define how to connect to server.
ip = '127.0.0.1'
port = 3000

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def login(sock):

    return

def createUser(sock):
    sock.send("createuser")
    user = raw_input("\nPlease type in your username: ")
    passWord = raw_input("\nPlease type in your password: ")
    group = raw_input("\nPlease type in your group name: ")

    sendData(sock, user)
    sendData(sock, passWord)
    sendData(sock, group)

    result = receiveData(sock)

    if (result == "newUserCreated"):
        return True
    return False


def uploadPrivateFile(sock) :
    message = raw_input("Please Type in what you'd like to send to the server: ")
    sendData(sock,message)
    return

def uploadPublicFile(sock) :
    return

def sendData(sock, message) :
    sock.send(message)
    waitForAck(sock)
    return

def receiveData(sock):
    print('waiting for response from server...')
    response = sock.recv(1024)
    print("response from server: {}".format(response))
    return response

def waitForAck(sock):
    response = s.recv(1024)
    if response == "ack":
        return
    else:
        print("Error in communication with the server.\nReceived: {}".format(response))
    return

if __name__ == '__main__':
    print('Server on {}:{}'.format(ip,port))

    # Connect to the server
    print('creating socket')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('connecting to server...')
    try:
        s.connect((ip, port))
    except:
        print("Server not found.")
        raw_input("Press ENTER to exit")
        exit()
    print("DONE\n")

    '''Login'''
    close = False
    while(close == False):
        print("Welcome to the secure file system (SFS)\nPlease select an option\n1: Login\n2: Create new user\n")
        sel = raw_input();
        if sel == '1':
            login(s)
        elif sel == '2':
            close = createUser(s)
        else:
            print("\nInvalid input\n")
        raw_input("\nPress Enter to continue.\n")
        cls()


    close = False
    while(close == False):
        print("Welcome to the secure file system (SFS)\nPlease select an option:\n1: Create/Open File\n2: Change Directory\n5: Exit")
        sel = raw_input();

        if sel == '1':
            uploadPrivateFile(s)
        elif sel == '2':
            uploadPublicFile(s)
        elif sel == '5':
            print("\nThe application will now close.\n")
            close = True
        else:
            print("\nInvalid input\n")
        raw_input("\nPress Enter to continue.\n")
        cls()

    '''
    # Send the data
    message = raw_input("Please Type in what you'd like to send to the server: ")
    print("sending data: {}".format(message))
    #len_sent = s.send(message)
    s.send(message)

    # Receive a response
    print('waiting for response...')
    #response = s.recv(len_sent)
    response = s.recv(1024)
    print("response from server: {}".format(response))
    '''
    # Clean up
    print('closing socket')
    s.close()
    print('done')