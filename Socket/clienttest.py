import client
import time


def pongEvent(data):
	print("Pong: " +str(time.time()-data))
	
def loginEvent(data):
	print("Erfolgreicher Login? "+str(data["erfolgreich"]))

client = client.Client("localhost",42069);

#while client.loggedin == False:
#	time.sleep(0.5)
	
print("vorbei")

client.on("pong", pongEvent)
client.on("login", loginEvent)

while True:
	client.emit("ping",time.time())
	time.sleep(60/1000)



while True:
	pass;