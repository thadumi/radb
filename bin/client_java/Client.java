/**
 * Client.java - client Java per il server RAEE
 *
 * @version 1.0 - 13 gen 16
 * @author  L.Calvi - Feltre
 *
 * implementazione di un client TCP mediante socket
 *
 */

import java.lang.*;
import java.io.*;
import java.net.*;

import java.util.concurrent.TimeUnit;

// oggetto che permette la connessione e comunicazione con un server (Python o altro)
public class Client
{
    private Socket socket = null;
    private BufferedReader reader = null;
    private BufferedWriter writer = null;

    public Client(String ip,int port) throws IOException
    {
        InetAddress address = InetAddress.getByName(ip);
        socket = new Socket(address, port);
        reader = new BufferedReader(new InputStreamReader(socket.getInputStream()));
        writer = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));
    } // [c] Client

    public void send(String msg) throws IOException
    {
        writer.write(msg, 0, msg.length());
        writer.flush();
    } // [m] send

    public String receive() throws IOException
    {
        //return reader.readLine();
        String ris = "";
        for (;;)
            {
            String line = reader.readLine();
            if (line.equals("<END>")) break;
            ris += line+'\n';
            }
        return ris;
    } // [m] receive

    public void close() throws IOException
    {
        reader.close();
        writer.close();
        socket.close();
    } // [m] close
   
} // [class] Client



class UsaClient
{
    public static void main(String[] args) throws IOException, InterruptedException
    {
        // connessione al server
        Client client = new Client("127.0.0.1",2468);
        System.out.println("[*] Client Java connesso al server!");

        String a[] = {
                      //"set dbpath ../db",           
                      "set dbpath ../../db",    //per eseguire localmente
                      "load CATALOG",
                      "get CATALOG",
                      "set DATABASES projection[Database] CATALOG",
                      "get DATABASES",
                      "set dbname azienda",
                   //   "load DIPENDENTE",
                   //   "load REPARTO",
                      "load *",
                      "get DIPENDENTE",
                      "get REPARTO",
                      "set R DIPENDENTE join[Reparto=Sigla] REPARTO",
                      "get R",
                      "set S selection[Reparto='P'] R",
                      "get S",
                      "set T projection[Cognome,Nome,Telefono] S",
                      "get T",
                      "close"
                     };

        // ciclo di comunicazione
        int nr = 0;
        try {
            for (int i=0; i<a.length; i++)
                {
                String s = a[i];

                // EVENTUALE CONVERSIONE: formato editor -> formato server
                // Ad esempio: 
                //   assegnazione "R<-Exp" convertita in "set R Exp"
                //   conversione dei caratteri pigreco, sigma, ... in project, ...
                //   ...

                System.out.println("[>] "+a[i]);
                client.send(s);
                if (s.equals("close")) break;
           //   System.out.println("In attesa di risposta dal server...");
                String response = client.receive();
                System.out.println("[<] " + response);
           //   TimeUnit.SECONDS.sleep(1);
                } // for
            }
        catch (IOException e)
            {
            System.out.println("Eccezione in UsaClient: " + e.toString());
            }

        client.close();
        System.out.println("Chiusa la connessione.\n");

    } // [m] main

} // [class] UsaClient


