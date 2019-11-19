import server


def spielerHandler(spieler):
	
	print("ja moin")
	
	def pingEvent(data):
		spieler.emit("pong",data)
	
	spieler.on("ping", pingEvent)
	
	spieler.emit("login", {"erfolgreich":True})



server = server.Server("localhost",42069);
server.onClientConnect = spielerHandler


while True:
	pass;