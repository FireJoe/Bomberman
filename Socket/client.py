import socket
import time
from _thread import start_new_thread
import json



class Client():
	def __init__(self,ip,port):
		print("Ip-Adresse: " + str(ip) + "\nPort: " + str(port))
		
		self.sock = socket.socket()
		self.sock.connect((ip, port))
		
		self.events = {}
		self.loggedin = False;
		self.starttime = time.time
		
		start_new_thread(self.mainLoop,())
		
	def mainLoop(self):
		try:
			while True:
				full_msg = ""
				maxlength = int(self.sock.recv(8).decode("utf-8"));
				
				while True:
					msg = self.sock.recv(min(8,maxlength-len(full_msg)))
					full_msg += msg.decode("utf-8")
					
					if(len(full_msg) == maxlength):
						self.receiveData(full_msg)
						break;
						
			
			
						
		except KeyboardInterrupt:
			_endtime = time.time()
			print("----------")
			print("Rip Server\nOnline for " + str(runden((_endtime-self.starttime)/60/60,3))+ " Hours")
			print("----------")
			self.sock.close();

			
	def emit(self,chanel,data):
		sendmsg = chanel +":"+json.dumps(data)
		length = len(sendmsg)
		self.sock.send(str(length).rjust(8).encode("utf-8"))
		
		self.sock.send(sendmsg.encode("utf-8"))
	
	def close(self):
		self.sock.close();
		
	def on(self,chanel,function):
		self.events[chanel] = function;
		
	def receiveData(self, data):
		data = data.split(":",1)
		chanel = data[0]
		data = json.loads(data[1])
		
		if(chanel == "login"):
			if(data["erfolgreich"] == True):
				self.loggedin = True;
				print("Erfolgreich eingeloggt!")
		
		if(chanel in self.events.keys()):
			self.events[chanel](data);
			
			
			
			
			
			
			