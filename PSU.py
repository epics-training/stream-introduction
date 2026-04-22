#!/usr/bin/env python3
# Original Copyright (C) 2010 Eric Norum
# Adapted for CODAC Core System Hands-on Training 

import socketserver
import random
import sys

try:
	port = int(sys.argv[1])
except:
	port = 24700

def clip(v):
	if (v > 10.0): return 10
	if (v < -10.0): return -10
	return v

status = { }
class DummyDevice(socketserver.StreamRequestHandler):
	def handle(self):
		global status
		client = self.client_address[0]
		if client not in status:
			status[client] = { }
			status[client]['volts'] = 0
			status[client]['on'] = False
		while 1:
			line = self.rfile.readline().strip()
			args = line.split()
			if (len(line) <= 0):
				break
			reply = None
			if (line == b'*IDN?'):
				reply = 'PSU-DEVICE-TXX'
			elif (line == b'POWER?'):
				reply = 'ON' if status[client]['on'] else 'OFF'
			elif (line == b'VSET?'):
				reply = '%.2f' % (status[client]['volts'])
			elif (line == b'VOUT?'):
				reply = '%.2f' % (status[client]['volts'] + random.uniform(-0.1, 0.1) if status[client]['on'] else 0)
			elif (len(args) > 1):
				try:
					if (args[0] == b'POWER' and args[1] == b'ON'):
						status[client]['on'] = True
						reply = 'POWER SWITCHED ON'
					elif (args[0] == b'POWER' and args[1] == b'OFF'):
						status[client]['on'] = False
						reply = 'POWER SWITCHED OFF'
					elif (args[0] == b'VSET'):
						status[client]['volts'] = clip(float(args[1]))
						reply = 'VOLTAGE SET TO %.2f' % (status[client]['volts'])
				except:
					pass
			if (reply):
				self.wfile.write(bytes(reply + '\r\n', 'utf-8'))

class Server(socketserver.ThreadingMixIn, socketserver.TCPServer):
	daemon_threads = True
	allow_reuse_address = True
	def __init__(self, server_address, RequestHandlerClass):
		socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass)

print ('Opening socket on port', str(port))

server = Server(('0.0.0.0', port), DummyDevice)

# Terminate with Ctrl-C
try:
	server.serve_forever()
except KeyboardInterrupt:
	sys.exit(0)
