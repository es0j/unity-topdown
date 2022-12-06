using System;
using System.IO;
using System.Net.Sockets;
using UnityEngine;
using System.Threading;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using Newtonsoft.Json;



public class NetObject
{
    public int id;
    public GameObject reference;
    public Queue<string>[] netPackets = new Queue<string>[Enum.GetValues(typeof(PcktType)).Length];
    
    public NetObject(GameObject gref){
        reference = gref;
        foreach (PcktType pType in Enum.GetValues(typeof(PcktType)))
        {
            netPackets[(int)pType] = new Queue<string>();
        }
    }

    public void DeliverPackets()
    {
        foreach (PcktType pType in Enum.GetValues(typeof(PcktType)))
        {
            foreach (string pkt in netPackets[(int)pType])
            {
                reference.GetComponent<PacketHandler>().HandlePacket(pType,pkt);        
            }
            netPackets[(int)pType].Clear();
        }
            
    }

    public void EnqueuePckt(PcktType t, string msg)
    {
        if (t == PcktType.PlayerInfo && netPackets[(int)t].Count == 1)
        {
            netPackets[(int)t].Dequeue();
        }
        netPackets[(int)t].Enqueue(msg);
       
    }
}

public class NetworkManager : MonoBehaviour
{
    [SerializeField]
    public GameObject[] entitiesTypes;
    
    private Thread rt;
    private Thread wt;
    
    private Stream s;
    private StreamReader sr;
    private StreamWriter sw;
    private int netId;
    

    private bool isRunning=true;
    
    private static Mutex mut = new Mutex();
    
    //holds reference to replicated netObjects
    private Dictionary<int, NetObject> netObjects = new Dictionary<int, NetObject>();
    
    //holds Packets to be processed as pEnter
    private Queue<PlayerEnter> pEnterList = new Queue<PlayerEnter>();
    
    //holds Packets to be processed as pEnter
    private Queue<PlayerLeave> pLeaveList = new Queue<PlayerLeave>();

    private PlayerInfo playerState = new PlayerInfo();
    private Queue<Packet> ActionsQueue = new Queue<Packet>(); 

    #region Singleton
    public static NetworkManager instance=null;
    void Awake()
    {
        if (instance != null)
        {
            Debug.LogWarning("more than one instance on equipment");
            return;
        }
        instance = this;
    }
    #endregion
    
    
    void Start()
    {
        Application.runInBackground = true;
        TcpClient client = new TcpClient();
        //client.ReceiveTimeout = 1000;
        if (!client.ConnectAsync("127.0.0.1", 9090).Wait(10000))
        {
            Debug.LogWarning("Failed to connect");
            return;
        }
        
        s = client.GetStream();
        sr = new StreamReader(s);
        sw = new StreamWriter(s);
        rt = new Thread(() => ReaderThread());
        wt = new Thread(() => WriterThread());
        
        
        //send first hand shake synchronous
        
        
        ClientHello p = new ClientHello();
        sw.WriteLine(p.ToJson(netId));
        sw.Flush();
        
        string msg = sr.ReadLine();
        ServerHello hello = JsonConvert.DeserializeObject<ServerHello>(msg);
        netId = hello.id;
        

        //start threads
        rt.Start();
        wt.Start();

    }

    private void Update()
    {
        try
        {
            mut.WaitOne();

            //deals with playerEntry
            foreach (PlayerEnter p in pEnterList)
            {
                Debug.Log("Spawning at: "+p.y+"+"+p.x);
                Vector3 newPosition = new Vector3(p.x,p.y);
        
                GameObject newObject = Instantiate(entitiesTypes[p.gid],newPosition,Quaternion.identity);
                netObjects[p.id] = new NetObject(newObject);
            }
            pEnterList.Clear();

            //deals with playerLeaving
            foreach (PlayerLeave p in pLeaveList)
            {
                Debug.Log("Despawining id=: "+p.id);
                Destroy( netObjects[p.id].reference);
                netObjects.Remove(p.id);
            }
            pLeaveList.Clear();
            
            //delivers packets to respective components
            foreach (NetObject n in netObjects.Values)
            {
                n.DeliverPackets();
            }
            
            mut.ReleaseMutex();
        }
        catch (Exception e)
        {
            Debug.LogError("Update: " + e);
            mut.ReleaseMutex();
            Destroy(gameObject);
        }

    }

    public void ReaderThread()
    {
        try
        {
            Debug.Log("ReaderThread start");
            while (isRunning)
            {
                string msg = sr.ReadLine();
                if (String.IsNullOrEmpty(msg))
                {
                    isRunning = false;
                    break;
                }

                mut.WaitOne();
                ParsePacket(msg);
                mut.ReleaseMutex();
            }
        }
        catch (Exception e)
        {
            Debug.LogError("ExceptionReader: " + e);
            mut.ReleaseMutex();
            s.Close();
        }
    }
    
    public void  WriterThread()
    {
        string lastState="";
        try
        {
            Debug.Log("WriterThread start");
            while (isRunning)
            {

                mut.WaitOne();

                foreach (Packet p in ActionsQueue)
                {
                    sw.WriteLine(p.ToJson(netId));
                }
                ActionsQueue.Clear();

                if (playerState != null)
                {
                    string newState = playerState.ToJson(netId);
                    if (lastState != newState)
                    {
                        sw.WriteLine(newState);
                    }
                    lastState = newState;
                }
                playerState = null;
                

                mut.ReleaseMutex();

                sw.Flush();
                Thread.Sleep(1000);
            }
        }
        catch (Exception e)
        {
            Debug.LogError("ExceptionWriter: "+ e);
            mut.ReleaseMutex();
            s.Close();
        }
    }

    public void SendAction(Packet packet)
    {
        mut.WaitOne();
        ActionsQueue.Enqueue(packet);
        mut.ReleaseMutex();
    }
    
    public void SendState(PlayerInfo p)
    {
        mut.WaitOne();
        playerState = p;
        mut.ReleaseMutex();
    }

    public void OnDestroy()
    {
       
        isRunning = false;
        mut.ReleaseMutex();
        s.Close();
        rt.Join();
        wt.Join();
        
    }


    public void ParsePacket(string msg)
    {
        Debug.Log("ParsePacket recved: "+msg);
        Packet p = JsonConvert.DeserializeObject<Packet>(msg);
        
        switch (p.type)
        {
            case PcktType.Error:
                Debug.LogError("Crash from gameserver: "+msg);
                break;
            case PcktType.PlayerEnter:
                PlayerEnter pEnter = JsonConvert.DeserializeObject<PlayerEnter>(msg);
                pEnterList.Enqueue(pEnter);
                break;
            case PcktType.PlayerLeave:
                PlayerLeave pLeave = JsonConvert.DeserializeObject<PlayerLeave>(msg);
                break;
            default:
                netObjects[p.id].EnqueuePckt(p.type,msg);
                break;
                
        }
        
        
        
    }
}


