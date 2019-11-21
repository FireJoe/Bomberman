import socket
import time
from _thread import start_new_thread
import json



class Client():
	def __init__(self,ip,port,reconnect=False,reconnecttime=5):
		print("Ip-Adresse: " + str(ip) + "\nPort: " + str(port))
		
		self.sock = socket.socket()
		self.sock.connect((ip, port))
		self.ip = ip;
		self.port = port;
		self.tryreconnect = reconnect;
		self.events = {}
		self.loggedin = False;
		self.starttime = time.time
		self.closed = False;
		self.ping = -1;
		self.onConnect = None;
		self.onReconnect = None;
		self.onClose = None;
		self.reconnecttime = reconnecttime
		
		
		start_new_thread(self.mainLoop,())
		start_new_thread(self.pingHandler,())
		
		
	def getPing(self):
		return self.ping;
		
	def pingHandler(self):
		def pongEvent(data):
			self.ping = round((time.time()-data)*1000);
			print("Pong: " +str(self.ping)+ "ms")
		self.events["pong"] = pongEvent
		
		while  not self.closed or self.tryreconnect:
			try:
				while self.emit("ping",time.time()):
					time.sleep(5)
			except ConnectionRefusedError:
				pass;
	
	
	def mainLoop(self):
		try:
			while not self.closed:
				full_msg = ""
				maxlength = int(self.sock.recv(64).decode("utf-8"));
				
				while True:
					msg = self.sock.recv(min(64,maxlength-len(full_msg)))
					full_msg += msg.decode("utf-8")
					
					if(len(full_msg) == maxlength):
						self.receiveData(full_msg)
						break;
						
		except Exception:
			time.sleep(1)
			if not self.closed:
				print("Verbindung zum Server Verloren!")
				if not self.closed:
					self.close();
				if(self.tryreconnect):
					self.reconnect();
				
	def isConnected(self):
		return self.loggedin
	
	def reconnect(self):
		self.loggedin = False;
		try:
			print("Starte Verbindungsversuch in "+str(self.reconnecttime)+" Sekunden...")
			time.sleep(self.reconnecttime)
			self.sock = socket.socket();
			self.sock.connect((self.ip, self.port))
			self.closed = False;
			if(self.onReconnect != None):
				self.onReconnect();
			self.mainLoop();
		except ConnectionRefusedError:
			self.reconnect();
			
			
			
	def emit(self,chanel,data):
		#print(self.closed)
		#print(self.tryreconnect)
		try:
			if ((not self.closed) or (not self.tryreconnect)):
				sendmsg = chanel +":"+json.dumps(data)
				length = len(sendmsg)
				self.sock.send(str(length).rjust(64).encode("utf-8"))
				
				self.sock.send(sendmsg.encode("utf-8"))
				return True;
		except ConnectionResetError:
			pass;
		return False;
	
	def close(self):
		if not self.closed:
			self.sock.close();
			self.closed = True;
			print("Der Client wurde ordnungsgemäß geschlossen!")
		else:
			print("Der Client wurde bereits geschlossen!")
			
		
	def on(self,chanel,function):
		self.events[chanel] = function;
		
	def receiveData(self, data):
		data = data.split(":",1)
		chanel = data[0]
		data = json.loads(data[1])
		print("chanel > " + chanel)
		if(chanel == "close"):
			self.loggedin = False;
			if(self.onClose != None):
				self.onClose();
		elif(chanel == "login" and self.loggedin == False):
			if(data["erfolgreich"] == True):
				self.loggedin = True;
				if(self.onConnect != None):
					self.onConnect();
		
		elif(chanel in self.events.keys()):
			self.events[chanel](data);
			
			
			
			
			
			
			