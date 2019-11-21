﻿# Multiplayer-Python-Bomberman #
### M.P.B. ###

### Socket: ###
* Server(server.Server(ip,port)) o
* Client (client.Client(ip,port,(reconnect=True,reconnecttime=5.0))) o
* Features:
	* Test-Programms ✔
	* Recieve Data based on length ✔
	* Auto-Reconnect für Client ✔
	* Standard-Funktion/-Events des Servers:
		* Close-Funktion (server.close())✔
	* Standard-Funktion/-Events des Clients:
		* Close-Funktion (client.close())✔
		* Ping/Pong-Funktion (client.getPing()) ✔
		* Connected-Funktion (client.isConnected()) ✔
		* Connect-Event (client.onConnect = Connect-Function) ✔
		* Reconnect-Event (client.onReconnect = Reconnect-Function) ✔
		* Close-Event (client.onClose = Close-Function) ✔
		
	


### Game: ###
* Jo
* Neh
* Geil


## Theorie: ##
* Spieler drückt (W,A,S,D,*Bombe legen*)
	* Eingabe wird an Server gesendet
		* Eingabe wird geprüft bzw. durchgeführt
			* Position/Richtung/Veränderung wird an alle geschickt
			* Erst dann bekommt Spieler die änderung mit
			
	


# Legende: #
##  : Planned ##
## o: In progress ##
## ◎: Complete and untested ##
## ✔: Complete and tested ##
