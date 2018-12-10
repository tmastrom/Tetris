from socket import *
from time import *
import random

HOST = '127.0.0.1'
PORT = 65432

print('Starting Server...')

#create a TCP/IP listening socket

s = socket(AF_INET, SOCK_STREAM)
s.bind((HOST,PORT))
s.listen(5)

print('listening for connections on port ', PORT)

#poll for clients trying to connect

print('searching for player 1')

while(True):
	p1, a1 = s.accept()
	if p1 != None:
		print('player 1 connected from port', str(a1))
		break

#poll for a second player

while(True):
	p2, a2 = s.accept()			
	if a2 != a1:		#make sure it is a different socket 
		print('player 2 connected from port ', str(a2))
		break

print('both players connected')

sleep(1)

print('waiting for players to ready up...')

s.setblocking(0)	#allow socket calls to return None


# Ready Sequence  
# Once both players have confirmed they are ready the game starts
while(True):

	try:
		p1_data = p1.recv(1024)
		print('player 1',p1_data)
	except: 
		pass

	try:
		p2_data = p2.recv(1024)
		print('player 2', p2_data)
	except:
		pass

	#send game start signal to both players
	p2.send(str(p1_data).encode('utf-8'))
	p1.send(str(p2_data).encode('utf-8'))
	print('sending start to both players')

	break

#Event Loop 
while(True):  

	#try to recv() data from each client
	try:
		p1_data = p1.recv(1024)
	except: 
		pass

	try:
		p2_data = p2.recv(1024)
	except:
		pass

	#typecast received data to int
	try:
		p1_data = int(p1_data)
	except:
		pass

	try:
		p2_data = int(p2_data)
	except:
		pass

	#send recv() data to the other client 
	p2.send(str(p1_data).encode('utf-8'))
	p1.send(str(p2_data).encode('utf-8'))

p1.close()
p2.close()

print('closed sockets')