import socket
import time
from _thread import start_new_thread
debug = True;
import json


def runden(wert,stellen): #zB: wert=12345.45546465 | stellen=2 | return=12345.46
	wert = wert*(10**stellen)
	wert = round(wert)/(10**stellen)
	return wert;

def debug(msg):
	if(debug):
		print(msg)



class Spieler():
	def __init__(self,server,con,addr):
		self.server = server;
		self.con = con;
		self.addr = addr;
		self.events = {};
		
	def emit(self,chanel,data):
		sendmsg = chanel +":"+json.dumps(data)
		length = len(sendmsg)
		self.con.send(str(length).rjust(64).encode("utf-8"))
		
		self.con.send(sendmsg.encode("utf-8"))
		
	def on(self,chanel,function):
		self.events[chanel] = function;
		
	def receiveData(self, data):
		data = data.split(":",1)
		chanel = data[0]
		data = json.loads(data[1])
		
		if(chanel in self.events.keys()):
			self.events[chanel](data);
		


class Server():
	def __init__(self,ip,port):
		print("Ip-Adresse: " + str(ip) + "\nPort: " + str(port))
		self.sock = socket.socket()
		
		self.sock.bind((ip, port))
		self.starttime = time.time()
		self.spieler = [];
		self.onClientConnect = None;
		self.closed = False;
		
		
		start_new_thread(self.ConnectionHandler,())
		start_new_thread(self.mainLoop,())

		
	def globalMsg(self,chanel,data):
		for sp in self.spieler:
			sp.emit(chanel,data)
			
	def close(self):
		if not self.closed:
			self.sock.close();
			self.closed = True;
			print("Der Server wurde ordnungsgemäß geschlossen!")
		else:
			print("Der Server wurde bereits geschlossen!")
		
	def mainLoop(self):
		try:
			while not self.closed:
				time.sleep(10)
				if not self.closed:
					debug("i am on: " + str(len(self.spieler)) + " Spieler")				
				else:
					break;
		except KeyboardInterrupt:
			self.sock.close();
			pass;
			
		_endtime = time.time()
		print("----------")
		print("Rip Server\nOnline for " + str(runden((_endtime-self.starttime)/60/60,3))+ " Hours")
		print("----------")
			
			
	def ClientHandler(self,sp):
		while True:
			try:
				full_msg = ""
				try:
					maxlength = int(sp.con.recv(64).decode("utf-8"));
					while True:
					
						msg = sp.con.recv(min(64,maxlength-len(full_msg)))
						full_msg += msg.decode("utf-8")
						
						if(len(full_msg) == maxlength):
							sp.receiveData(full_msg)
							break;
							
				except ConnectionResetError:
					if sp in self.spieler:
						self.spieler.remove(sp);
					break;
			except Exception as ex:
				print("--------------------clienthandler")
				print(ex)
				print("--------------------clienthandler")
				break;
			
	def ConnectionHandler(self):
		while True:
			try:
				print("Warte auf Verbindung....")
				self.sock.listen(1)
				
				con, addr = self.sock.accept()
				
				sp = Spieler(self,con,addr)
				
				self.spieler.append(sp)
				if(self.onClientConnect != None):
					self.onClientConnect(sp)
					
				start_new_thread(self.ClientHandler,(sp,))
			except Exception as ex:
				break;
			



