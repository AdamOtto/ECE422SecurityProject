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


def createUser(handler):
    print("Now in the createUser function")

    userName = receiveData(handler)
    handler.logger.debug('userName:recv()->"%s"', userName)
    password = receiveData(handler)
    password=cryp_file.dcry_fdata(password,"test")
    handler.logger.debug('password:recv()->"%s"', password)
    groupName = receiveData(handler)
    handler.logger.debug('groupName:recv()->"%s"', groupName)

    #Create userID
    f=sh.open_user()
    data=f["data"]
    uid = np.max(data['uid'])+1
    handler.logger.debug('userID->"%s"', uid)

    #Create User
    result = sh.reg_user(uid, userName, password, groupName)
    handler.logger.debug('result->"%s"', result)

    if(result == "sucess"):
        sendData(handler,"newUserCreated")
        sendData(handler,uid)
    return

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
    return


def sendAck(handler):
    handler.request.send("ack")

def waitForAck(handler):
    response = handler.request.recv(SendReceiveSize)
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
