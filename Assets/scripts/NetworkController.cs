using System;
using System.IO;
using System.Net.Sockets;
using UnityEngine;
using System.Threading;

class NetworkController{
    public void Connect(string server,int port){
        TcpClient client = new TcpClient(server,port);

        
        Stream s = client.GetStream();
        StreamReader sr = new StreamReader(s);
        StreamWriter sw = new StreamWriter(s);
        
        
        Thread rt = new Thread(() => ReaderThread(sr));
        Thread wt = new Thread(() => WriterThread(sw));
        
        rt.Start();
        wt.Start();
        
    }

    public void ReaderThread(StreamReader s)
    {
        while (true)
        {
            string msg = s.ReadLine();
            Debug.Log("Recived Message " + msg );    
        }
        
    }

    public void WriterThread(StreamWriter s)
    {
        
    }
}