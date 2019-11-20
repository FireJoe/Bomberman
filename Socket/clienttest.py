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



client = client.Client("localhost",42069,reconnect=True);

#while client.loggedin == False:
#	time.sleep(0.5)

client.onReconnect = onReconnectHandler
client.onConnect = onConnectHandler

client.on("testlist", testlistEvent)

client.emit("testlist", ["123","789","456"])



try:	
	while True:
		pass;
except KeyboardInterrupt:
	client.close();


