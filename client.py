"""
References:
    https://pymotw.com/2/SocketServer/
"""
import logging
import sys
import socket

#Define how to connect to server.
ip = '127.0.0.1'
port = 3000

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

    # Clean up
    print('closing socket')
    s.close()
    print('done')
    raw_input('Press ENTER to exit')