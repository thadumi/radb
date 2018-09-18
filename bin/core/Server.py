# File: Server.py
# Date: 20 gen 16
# Note: esempio di server socket che comunica con piu' client

import socket
from _thread import start_new_thread

import time 

HOST = ''      # all availabe interfaces
PORT = 2468    # porta di ascolto del server
MSGLEN = 10000 #4056  # lunghezza massima dei messaggi
  
class Server:
    "oggetto server di una connessione"

    # crea il socket per la comunicazione
    def __init__(self):
        self.servername = 'Server RAEE - ver. 20 gen 16'
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
               
    # attiva il server che si mette in ascolto sulla porta
    def active(self,nporta):
        self.serversocket.bind(('localhost', nporta))
        self.serversocket.listen(5) # socket con al massimo 5 connessioni
        print('[-] Server waiting on',nporta,'port for a connection ...')
        while True:
            # blocking call, waits to accept a connection
            conn, addr = self.serversocket.accept()
            self.clientname = addr[0] + ":" + str(addr[1])
            print("[-] Connected to " + self.clientname)
            start_new_thread(self.client_thread, (conn,self.clientname)) 

    def client_thread(self,conn,clientname):
        #self._send(conn,"Welcome to the Server\n")
        self._send(conn,self.servername)
        while True:
            data = self._receive(conn)
            if data == 'close': break
            print('[from '+clientname +'>]',data)
            reply = self.execute(data)
            #reply += '<END>\n'  # terminatore per Java
            self._send(conn,reply)
            #time.sleep(2) 
        conn.close()
        print("[-] Disconnected client " + self.clientname)

    # ritorna il messaggio che riceve dalla connessione conn    
    def _receive(self,conn):
        buf = conn.recv(MSGLEN)
        buf = buf.decode('utf-8')
        return buf
   
    # elaborazione della richiesta: ritorna il risultato dell'elaborazione
    # per default, ritorna la richiesta in maiuscolo (metodo da sovrascrivere)
    def execute(self,query):
        #print('CHIAMATA ServerMulti.execute!!!!!!!!!!!!!!')
        #return query.upper()+'\nnew_exec penultima riga\n'+'ultima riga.\n' # provvisorio
        return query.upper()
        #pass
    
    # invia sulla connessione con il messaggio msg
    def _send(self,conn,msg):
        s = msg.encode('utf-8')
        #conn.sendall(s)
        conn.send(s)

    def close(self):
       self.serversocket.close() 

#---- main ----
if __name__ == "__main__":
    serv = Server()
    serv.active(PORT)

