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
				while True:
					msg = self.sock.recv(8)
					full_msg += msg.decode("utf-8")
					
					if len(msg) <= 0 or msg == " " or full_msg.endswith(" "):
						if len(full_msg) > 0:
							self.receiveData(full_msg)
						break
						
		except KeyboardInterrupt:
			_endtime = time.time()
			print("----------")
			print("Rip Server\nOnline for " + str(runden((_endtime-self.starttime)/60/60,3))+ " Hours")
			print("----------")
			self.sock.close();

			
	def emit(self,chanel,data):
		sendmsg = chanel +":"+json.dumps(data)
		self.sock.send(sendmsg.encode("utf-8"))
		self.sock.send(b" ")
		
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
		
		elif(chanel in self.events.keys()):
			self.events[chanel](data);
			
			
			
			
			
			
			