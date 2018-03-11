"""
References:
    https://pymotw.com/2/SocketServer/
"""
import time
import logging
import sys
import socket
import os
import atexit
#import cryp_file
#Define how to connect to server.
ip = '127.0.0.1'
port = 3000
#Global Variables
SendReceiveSize = 4096
userId = ""
userName = ""
userGroup = ""
directory = ""

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def login(sock):
    sock.send("login")
    waitForAck(sock)

    user = raw_input("\nPlease type in your username: ")
    sendData(sock, user)
    passWord = raw_input("\nPlease type in your password: ")
    sendData(sock, passWord)

    result = receiveData(sock)

    if (result == "success"):
        print("Login successful\n")

        global userId
        userId = receiveData(sock)
        global userName
        userName = receiveData(sock)
        global userGroup
        userGroup = receiveData(sock)
        global directory
        directory = "/"

        return True
    else:
        print("Login unsuccessful.  Make sure you typed in your username and password correctly\n")
        return False

def createUser(sock):
    sock.send("createuser")
    waitForAck(sock)

    user = raw_input("\nPlease type in your username: ")
    passWord = raw_input("\nPlease type in your password: ")
    group = raw_input("\nPlease type in your group name: ")
    f=open("ctest.txt")
    #newPassword = cryp_file.cry_fdata(f, group)

    sendData(sock, user)
    #sendData(sock, newPassword)
    sendData(sock, passWord)
    sendData(sock, group)

    result = receiveData(sock)

    if (result == "newUserCreated"):
        global userId
        userId = receiveData(sock)
        global userName
        userName = user
        global userGroup
        userGroup = group
        global directory
        directory = "/"
        return True
    return False


def uploadPrivateFile(sock) :
    global userId
    global directory

    sock.send("createFile")

    title = raw_input("File name: ")
    sendData(sock, title)
    message = raw_input("Please Type in what you'd like to send to the server: ")
    sendData(sock, message)
    time.sleep(0.1)
    sendData(sock,userId)
    time.sleep(0.1)
    sendData(sock, directory)

    time.sleep(0.1)

    result = receiveData(sock)

    return


def listAllFiles(sock) :
    sock.send("listFiles")

    return


def changeDirectory(sock):

    return


def readFile(sock):
    return


def editFile(sock):
    return


def sendData(sock, message) :
    if (isinstance(message, int) or isinstance(message, float)):
        temp = str(message)
        sock.send(temp)
    else:
        sock.send(message)
    waitForAck(sock)
    return

def receiveData(sock):
    print('waiting for response from server...')
    response = sock.recv(SendReceiveSize)
    sendAck(sock)
    print("response from server: {}".format(response))
    return response

def sendAck(sock):
    sock.send("ack")

def waitForAck(sock):
    response = sock.recv(3)
    if response == "ack":
        print("Received ack\n")
        return
    else:
        print("Error in communication with the server.\nReceived: {}".format(response))
    return

def exit_handler():
    print('closing socket')
    s.close()
    print('done')

if __name__ == '__main__':
    print('Server on {}:{}'.format(ip,port))
    atexit.register(exit_handler)

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
    '''
    close = False
    while(close == False):
        print("Welcome to the secure file system (SFS)\nPlease select an option\n1: Login\n2: Create new user\n")
        sel = raw_input();
        if sel == '1':
            close = login(s)
        elif sel == '2':
            close = createUser(s)
        else:
            print("\nInvalid input\n")
        raw_input("\nPress Enter to continue.\n")
        cls()
    '''

    '''For testing only'''
    userId = 0
    userGroup = "test"
    userName = "test"
    directory = "/"
    close = False
    while(close == False):
        print("Welcome to the secure file system (SFS)\nUserID: {}, Username: {}, Group: {}, Directory: {}\n"
              "Please select an option:\n"
              "1: Create a file in current directory\n"
              "2: Change directory\n"
              "3: List all files\n"
              "4: Read a file\n"
              "5: Edit a file\n"
              "7: Exit"
              .format(userId, userName, userGroup, directory))
        sel = raw_input();

        if sel == '1':
            uploadPrivateFile(s)
        elif sel == '2':
            changeDirectory(s);
        elif sel == '3':
            listAllFiles(s);
        elif sel == '4':
            readFile(s);
        elif sel == '5':
            editFile(s);
        elif sel == '7':
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
    response = s.recv(SendReceiveSize)
    print("response from server: {}".format(response))
    '''
    # Clean up
    print('closing socket')
    s.close()
    print('done')
