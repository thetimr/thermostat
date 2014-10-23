#!/usr/bin/python

import socket
import sys
import time
import signal

from Queue import Queue
from threading import Thread
from thread import *

from utils import StoppableThread

HOST = ''
PORT = 8888

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print "socket created"

try:
	s.bind((HOST,PORT))
except socket.error , msg:
	print 'Bind failed. Error Code: ' + str(msg[0]) + 'Message ' + msg[1]
	sys.exit()

print "socket bind complete"


s.listen(10)
print 'Socket now listening'

class Controller(StoppableThread):

	def __init__(self):
		super(Controller, self).__init__()
		self.clients = []
		self.TempClients = []

	def addClient(self, client):
		self.clients.append(client)

	def regTempClient(self, client):
		self.TempClients.append(client)

	def sendToTempClients(self, data):
		print 'sendtotempclients'
		for client in self.TempClients:
			print 'sending to a temp client'
			client.addData(data)
			print 'Sent data to client'

	def stop(self):
		super(Controller, self).stop()

		for client in self.clients:
			print "Stopping a client"
			client.stop()
		for client in self.clients:	
			print "joining a client"
			client.join()
		print "done stopping"

	def run(self):
		while self.isRunning():
			self.sleep(5)
			print "Controller thread running..."


myController = Controller()
myController.start()


#Function for handling connections
class clientThread(StoppableThread):

	def __init__(self, conn):
		super(clientThread, self).__init__()
		self.conn = conn
		self.EventData = Queue()

	def receivedData(self, data):
		reply = 'Message Received at the server!\n'
		if data == "Reg: Temp":
			# Register to receive temp data
			myController.regTempClient(self)
		else:
			myController.sendToTempClients(data)
			print 'sent temp to controller ' + data + ' ' + str(self.conn.getpeername()[1])
		print data + ' ' + str(self.conn.getpeername()[1])
		self.conn.sendall(reply)

	# Put in Queue
	def addData(self, data):
		print 'adding data to client '+ str(self.conn.getpeername()[1])
		self.EventData.put(data)
		print 'adddded data '+ str(self.conn.getpeername()[1])

	def checkForData(self):
		print 'checking for data ' + str(self.conn.getpeername()[1])
		if not self.EventData.empty():
			print 'data found '+ str(self.conn.getpeername()[1])
			data = self.EventData.get()
			self.conn.sendall(data)
			print 'data sent '+ str(self.conn.getpeername()[1])
		

	def run(self):

		self.conn.settimeout(1)
		#Sending message to connected client
		self.conn.send('Welcome to the server.\n') #send only takes string

		#infinite loop so that function do not terminate and thread do not end.
		while self.isRunning():
			print 'looping ' + str(self.conn.getpeername())

			try:
				#Receiving from client
				data = self.conn.recv(1024)
				if data:
					self.receivedData(data)
					print 'done data RRR ' + str(self.conn.getpeername()[1])
			except socket.timeout:
				pass
			print 'to check for data ' + str(self.conn.getpeername()[1])
			self.checkForData()	        

		print 'CLOSING '+ str(self.conn.getpeername()[1])
		self.conn.close()


# Run Server
try: 
	#now keep talking with the client
	while 1:
	    #wait to accept a connection
	    conn, addr = s.accept()
	    print 'Connected with ' + addr[0] + ':' + str(addr[1])

	    client = clientThread(conn)
	    myController.addClient(client)
	    client.start()
	    #start new thread
	    #start_new_thread(clientthread ,(conn,))
except KeyboardInterrupt:
	 print 'Quitting'

s.close()
myController.stop()
myController.join()

print 'done'
