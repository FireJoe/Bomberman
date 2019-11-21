import client
import time


def onReconnectHandler():
	print("Verbindung wiederhergestellt")
	
def onConnectHandler():
	print("Verbindung hergestellt")

def testlistEvent(data):
	print(data[0])
	print(data[1])
	print(data[2])

def onCloseHandler():
	print("Server wurde geschlossen...")

client = client.Client("localhost",42069,reconnecttime=0.5);


client.onReconnect = onReconnectHandler
client.onConnect = onConnectHandler
client.onClose = onCloseHandler

client.on("testlist", testlistEvent)

client.emit("testlist", ["123","789","456"])



try:	
	while not client.isConnected():
		pass
	while client.isConnected():
		pass;
except KeyboardInterrupt:
	client.close();


