"""
References:
    https://pymotw.com/2/SocketServer/
"""
import logging
import sys
sys.path.append("C:\Users\adamo\School\ECE 422\ECE422SecurityProject")
import SocketServer
import storage_h5 as sh
import numpy as np
import cryp_file
SendReceiveSize = 4096

logging.basicConfig(level=logging.DEBUG,
                    format='%(name)s: %(message)s',
                    )


class EchoRequestHandler(SocketServer.BaseRequestHandler):

    def __init__(self, request, client_address, server):
        self.logger = logging.getLogger('EchoRequestHandler')
        self.logger.debug('__init__')
        SocketServer.BaseRequestHandler.__init__(self, request, client_address, server)
        return

    def setup(self):
        self.logger.debug('setup')
        return SocketServer.BaseRequestHandler.setup(self)

    #This function handles all requests from the user.
    #For each request from the user, the first .
    def handle(self):
        exit = False
        while(exit == False):
            self.logger.debug('handle')

            # Only allows input to be 1Kb long.  Can be made longer later
            data = self.request.recv(SendReceiveSize)
            sendAck(self)
            self.logger.debug('recv()->"%s"', data)
            if(data == ""):
                exit = True
            elif data == "createuser":
                createUser(self)
            elif data == "login":
                login(self)
            elif data == "createFile":
                createFile(self)
            elif data == "listFiles":
                listAllFiles(self)
            elif data == "changeDirectory":
                changeDirectory(self)
            elif data == "createDirectory":
                createDirectory(self)
            elif data == "readFile":
                readFile(self)
            elif data == "editFile":
                editFile(self)

            #self.request.send(data)
            #self.request.sendall("Thank you, we have received your '{}' message.".format(data))

        return

    def finish(self):
        self.logger.debug('finish')
        return SocketServer.BaseRequestHandler.finish(self)


class EchoServer(SocketServer.TCPServer):

    def __init__(self, server_address, handler_class=EchoRequestHandler):
        self.logger = logging.getLogger('EchoServer')
        self.logger.debug('__init__')
        SocketServer.TCPServer.__init__(self, server_address, handler_class)
        return

    def server_activate(self):
        self.logger.debug('server_activate')
        SocketServer.TCPServer.server_activate(self)
        return

    def serve_forever(self):
        self.logger.debug('waiting for request')
        self.logger.info('Handling requests, press <Ctrl-C> to quit')
        while True:
            self.handle_request()
        return

    def handle_request(self):
        self.logger.debug('handle_request')
        return SocketServer.TCPServer.handle_request(self)

    def verify_request(self, request, client_address):
        self.logger.debug('verify_request(%s, %s)', request, client_address)
        return SocketServer.TCPServer.verify_request(self, request, client_address)

    def process_request(self, request, client_address):
        self.logger.debug('process_request(%s, %s)', request, client_address)
        return SocketServer.TCPServer.process_request(self, request, client_address)

    def server_close(self):
        self.logger.debug('server_close')
        return SocketServer.TCPServer.server_close(self)

    def finish_request(self, request, client_address):
        self.logger.debug('finish_request(%s, %s)', request, client_address)
        return SocketServer.TCPServer.finish_request(self, request, client_address)

    def close_request(self, request_address):
        self.logger.debug('close_request(%s)', request_address)
        return SocketServer.TCPServer.close_request(self, request_address)

'''
Create User

Allows for a new user to register on the database.
'''
def createUser(handler):
    print("Now in the createUser function")

    userName = receiveData(handler)
    handler.logger.debug('userName:recv()->"%s"', userName)
    password = receiveData(handler)
    #password=cryp_file.dcry_fdata(password,"test")
    handler.logger.debug('password:recv()->"%s"', password)
    groupName = receiveData(handler)
    handler.logger.debug('groupName:recv()->"%s"', groupName)

    #Create userID
    f=sh.open_user()
    data=f["data"]
    uid = np.max(data['uid'])+1
    handler.logger.debug('userID->"%s"', uid)

    #Create User
    print("Trying to create user...")
    result = sh.reg_user(uid, userName, password, groupName)
    handler.logger.debug('result->"%s"', result)

    if(result == "sucess"):
        sendData(handler,"newUserCreated")
        sendData(handler,uid)

    print("Exiting CreateUser")
    return

'''
Login

Allows an existing user to log in.
'''
def login(handler):
    print("Now in the login function")

    userName = receiveData(handler)
    handler.logger.debug('userName:recv()->"%s"', userName)
    password = receiveData(handler)
    handler.logger.debug('password:recv()->"%s"', password)

    print("username and password received\n")

    #Check if user exists
    result = sh.log_in(userName,password)

    print("result:{}".format(result))

    if (result != (None, None, None)):
        print("Login Successful\n")
        sendData(handler,"success")

        sendData(handler, result[0])
        sendData(handler, result[1])
        sendData(handler, result[2])
    else:
        print("Login failed\n")
        sendData(handler,"Fail")
    print("Exiting login function")
    return

'''
create file

Creates a file on the database under the users current directory
'''
def createFile(handler):
    print("in CreateFile function")
    f = sh.open_public()

    fileName = receiveData(handler)
    handler.logger.debug('userName:recv()->"%s"', fileName)
    message = receiveData(handler)
    handler.logger.debug('userName:recv()->"%s"', message)
    userID = receiveData(handler)
    handler.logger.debug('userName:recv()->"%s"', userID)
    directory = receiveData(handler)
    handler.logger.debug('userName:recv()->"%s"', directory)



    result = sh.write_h5(f, int(userID), fileName, directory, message)

    print(result)
    if result is None:
        sendData(handler, "FAILURE: File NOT created.")
    else:
        sendData(handler, "success")
    print("Exiting createFile...")
    return

'''
List all files

Lists all files and folders in the user's current directory
'''
def listAllFiles(handler):
    print("Now in listAllFiles function.")

    directory = receiveData(handler)
    handler.logger.debug('userName:recv()->"%s"', directory)

    f = sh.open_public()
    result = sh.list_h5(f, directory)
    print(result)

    for r in result:
        sendData(handler, r)
    sendData(handler, "-#-done-#-")
    return

'''
Change Directory

Allows the user to change their directory and read files of other users.
'''
def changeDirectory(handler):
    print("Now in changeDirectory function.")

    currDir = receiveData(handler)
    handler.logger.debug('userName:recv()->"%s"', currDir)
    newDir = receiveData(handler)
    handler.logger.debug('userName:recv()->"%s"', newDir)

    if newDir == "/":
        sendData(handler, "/")
        return

    if(currDir != "/"):
        newDir = "/" + newDir

    '''Check if newDir exists'''
    f = sh.open_public()
    result = sh.list_h5(f, currDir)

    if (currDir + newDir) in result:
        sendData(handler, (currDir + newDir))
    else:
        sendData(handler, "-#-fail-#-")

    return

'''
Create Directory

Create a new directory in the database.
'''
def createDirectory(handler):
    print("Now in createDirectory function.")


    currDir = receiveData(handler)
    handler.logger.debug('userName:recv()->"%s"', currDir)
    newDir = receiveData(handler)
    handler.logger.debug('userName:recv()->"%s"', newDir)

    f = sh.open_public()
    result = sh.create_directory(f, newDir, loc = currDir)

    if(result == "success!"):
        sendData(handler, result)
    else:
        sendData(handler, "ERROR: Directory not created...")
    return

'''
Read File

Used to read a file on the database.  Cannot read a file from a different group.
'''
def readFile(handler):
    print("Now in readFile function.")

    currDir = receiveData(handler)
    handler.logger.debug('userName:recv()->"%s"', currDir)
    currUserID = receiveData(handler)
    handler.logger.debug('userName:recv()->"%s"', currUserID)
    fileName = receiveData(handler)
    handler.logger.debug('userName:recv()->"%s"', fileName)


    f = sh.open_public()
    fUser = sh.open_user()
    users = sh.read_h5(fUser,"/")
    currGrp = users[users['uid'] == int(currUserID)]['group']
    result = sh.read_h5(f, currDir)
    re = result[result['fname']==fileName]
    if(re != None):
        fuid = re['uid']
        fgroup = users[users['uid'] == fuid]['group']
        if fgroup != currGrp:
            sendData(handler, "You are not allowed to access this file!")
            return
        sendData(handler, re['context'][0])
    else:
        sendData(handler,"File does not exist.")
    return

'''
Edit File

Used to edit a file on the database.
'''
def editFile(handler):
    print("Now in editFile function.")

    currUID = receiveData(handler)
    currDir = receiveData(handler)
    fileName = receiveData(handler)

    f = sh.open_public()
    result = sh.list_h5(f, currDir)

    if(fileName in result):
        re = sh.read_h5(f, currDir)
        if int(currUID) == re[re['fname']==fileName]['uid']:

            sendData(handler, "CanWrite")
            sendData(handler, re[re['fname']==fileName]['context'][0])
            newMessage = receiveData(handler)
            result = sh.write_h5(f, int(currUID), fileName, currDir, newMessage)
            print(result)
            if result is None:
                sendData(handler, "FAILURE: File NOT edited.")
            else:
                sendData(handler, "success")
        else:
            sendData(handler, "Permission Denied.")
    else:
        sendData(handler, "File doesn't exist.")

    return

def sendAck(handler):
    handler.request.send("ack")

def waitForAck(handler):
    response = handler.request.recv(3)
    if response == "ack":
        print("received ack\n")
        return
    else:
        print("Error in communication with the client.\nReceived: {}".format(response))
    return

def sendData(handler, message) :
    type(message)
    if( isinstance(message, int) or isinstance(message, float) ):
        temp = str(message)
        handler.request.send(temp)
    else:
        handler.request.send(message)
    waitForAck(handler)
    return

def receiveData(handler):
    print('waiting for response from client...')
    response = handler.request.recv(SendReceiveSize)
    sendAck(handler)
    print("response from client: {}".format(response))
    return response


if __name__ == '__main__':
    import socket
    import threading

    address = ('localhost', 3000)  # let the kernel give us a port
    server = EchoServer(address, EchoRequestHandler)
    ip, port = server.server_address  # find out what port we were given
    print("ip = {}\nport = {}".format(ip,port))
    t = threading.Thread(target=server.serve_forever)
    t.setDaemon(True)  # don't hang on exit
    t.start()
    raw_input('Press ENTER to shut down server\n')
    server.socket.close()
"""
    logger = logging.getLogger('client')
    logger.info('Server on %s:%s', ip, port)

    # Connect to the server
    logger.debug('creating socket')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logger.debug('connecting to server')
    s.connect((ip, port))

    # Send the data
    message = 'Hello, world'
    logger.debug('sending data: "%s"', message)
    len_sent = s.send(message)

    # Receive a response
    logger.debug('waiting for response')
    response = s.recv(len_sent)
    logger.debug('response from server: "%s"', response)

    # Clean up
    logger.debug('closing socket')
    s.close()
    logger.debug('done')
    input('Press ENTER to exit\n')
    server.socket.close()
"""
