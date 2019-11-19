import client
import time


def pongEvent(data):
	print("Pong: " +str(round((time.time()-data)*1000))+ "ms")
	
def loginEvent(data):
	print("Erfolgreicher Login? "+str(data["erfolgreich"]))
	
def testlistEvent(data):
	print(data)



client = client.Client("localhost",42069);

#while client.loggedin == False:
#	time.sleep(0.5)
	
print("vorbei")

client.on("pong", pongEvent)
client.on("login", loginEvent)
client.on("testlist", testlistEvent)

client.emit("testlist", ["123","789","456"])

while True:
	client.emit("ping",time.time())
	time.sleep(5)
	client.close();



while True:
	pass;