import server


def spielerHandler(spieler):
	
	def pingEvent(data):
		spieler.emit("pong",data)
	
	def testlistEvent(data):
		spieler.emit("testlist",data)
	
	spieler.on("ping", pingEvent)
	spieler.on("testlist", testlistEvent)
	spieler.emit("login", {"erfolgreich":True})



server = server.Server("localhost",42069);
server.onClientConnect = spielerHandler



running = True;
try:
	while running:
		pass;
except KeyboardInterrupt:
	running = False;
	server.close();
	
