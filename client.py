import socket
import sys
import time
import config

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = (config.c['server_addr'], config.c['server_port'])
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)

try:
    
    while 1:
    
	    # Send data
	    message = '{"accelerometer":"15.45","speed":"21","gps":"45.5485N 48.45865E"}'
	    print >>sys.stderr, 'sending "%s"' % message
	    sock.sendall(message)

	    # Look for the response
	    amount_received = 0
	    amount_expected = 2 # 'ok'
	    
	    while amount_received < amount_expected:
	        data = sock.recv(32)
	        amount_received += len(data)
	        print >>sys.stderr, 'received "%s"' % data

	   	time.sleep(3) # wait 5 seconds for next packet to send

finally:
    print >>sys.stderr, 'closing socket'
    sock.close()