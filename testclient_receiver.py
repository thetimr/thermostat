#!/usr/bin/python

import socket   
import sys  
import struct
import time

#main function
if __name__ == "__main__":

    if(len(sys.argv) < 2) :
        print 'Usage : python client.py hostname'
        sys.exit()

    host = sys.argv[1]
    port = 8888

#create an INET, STREAMing socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print 'Failed to create socket'
    sys.exit()

print 'Socket Created'

try:
    remote_ip = socket.gethostbyname( host )
    s.connect((host, port))

except socket.gaierror:
    print 'Hostname could not be resolved. Exiting'
    sys.exit()

print 'Socket Connected to ' + host + ' on ip ' + remote_ip

#Receive Data
try :
    #Register for temp
    s.send("Reg: Temp")
    print 'Sent Reg: Temp'
except socket.error:
    #Send failed
    print 'Send failed'
    sys.exit()


try :
    #Set the whole string
    while True:
        resp = s.recv(1024)
        print resp
        time.sleep(1)
        print 'Looping...'
except socket.error:
    #Send failed
    print 'Send failed'
    sys.exit()


s.close()