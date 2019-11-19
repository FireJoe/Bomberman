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
		#print("emit: " + chanel + "\ndata:" + str(data))
		sendmsg = chanel +":"+json.dumps(data)
		self.con.send(sendmsg.encode("utf-8"))
		self.con.send(b" ")
		
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
		
		start_new_thread(self.ConnectionHandler,())
		start_new_thread(self.mainLoop,())
		
	def mainLoop(self):
		try:
			while True:
				time.sleep(10)
				debug("i am on: " + str(len(self.spieler)) + " Spieler")				
		except KeyboardInterrupt:
			_endtime = time.time()
			print("----------")
			print("Rip Server\nOnline for " + str(runden((_endtime-self.starttime)/60/60,3))+ " Hours")
			print("----------")
			self.sock.close();
			
	def ClientHandler(self,spieler):
		while True:
			#debug("still there... "+str(spieler.addr))
			#time.sleep(5)
			
			full_msg = ""
			while True:
				
				msg = spieler.con.recv(8)
				full_msg += msg.decode("utf-8")
				
				if len(msg) <= 0 or msg == " " or full_msg.endswith(" "):
					if len(full_msg) > 0:
						spieler.receiveData(full_msg)
					break
			
			
			
			
	
	def globalMsg(self,chanel,data):
		for sp in self.spieler:
			sp.emit(chanel,data)
			
	def ConnectionHandler(self):
		while True:
			print("Warte auf Verbindung....")
			self.sock.listen(1)
			
			con, addr = self.sock.accept()
			
			sp = Spieler(self,con,addr)
			
			self.spieler.append(sp)
			if(self.onClientConnect != None):
				self.onClientConnect(sp)
				
			start_new_thread(self.ClientHandler,(sp,))
			
			



