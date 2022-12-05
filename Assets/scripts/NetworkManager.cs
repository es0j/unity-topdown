using System;
using System.IO;
using System.Net.Sockets;
using UnityEngine;
using System.Threading;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using Newtonsoft.Json;
using UnityEngine;
using UnityEngine.Networking.Types;



   
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

    //states to send
    private PlayerInfo playerState = new PlayerInfo();
    private Queue<Packet> ActionsQueue = new Queue<Packet>(); 

    private bool isRunning=true;
    
    private static Mutex mut = new Mutex();
    
    private Dictionary<int, GameObject> netObjects = new Dictionary<int, GameObject>();
    private Dictionary<int,PlayerInfo> pInfoList = new Dictionary<int, PlayerInfo>();
    private Queue<PlayerEnter> pEnterList = new Queue<PlayerEnter>();


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
        TcpClient client = new TcpClient();
        //client.ReceiveTimeout = 1000;
        if (!client.ConnectAsync("127.0.0.1", 9090).Wait(1000))
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

            foreach (PlayerEnter p in pEnterList)
            {
                HandlePlayerEnter(p);
            }

            pEnterList.Clear();

            foreach (int p in pInfoList.Keys)
            {
                HandlePInfo(pInfoList[p]);
            }

            pInfoList.Clear();


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
            Debug.LogError("ExceptionWriter: {0}"+ e);
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
            case PcktType.PlayerInfo:
                PlayerInfo pInfo =  JsonConvert.DeserializeObject<PlayerInfo>(msg);
                pInfoList[p.id]=pInfo;
                break;
            case PcktType.PlayerEnter:
                PlayerEnter pEnter = JsonConvert.DeserializeObject<PlayerEnter>(msg);
                pEnterList.Enqueue(pEnter);
                break;
            default:
                Debug.LogWarning("Unknown packet:"+msg);
                break;
                
        }
        
        
        
    }

    public void HandlePInfo(PlayerInfo p)
    {
        Vector3 newPosition = new Vector3(p.x,p.y);
        if (netObjects.ContainsKey(p.id))
        {
            netObjects[p.id].transform.position = newPosition;    
        }
        else
        {
            Debug.LogWarning("Recivigin update for unexisted netobject");
        }
        
    }
    
    public void HandlePlayerEnter(PlayerEnter p)
    {
        Debug.Log("Spawning at: "+p.y+"+"+p.x);

        GameObject newObject = Instantiate(entitiesTypes[p.gid]);
        netObjects[p.id] = newObject;
        Vector3 newPosition = new Vector3(p.x,p.y);
        netObjects[p.id].transform.position = newPosition;
        
    }
}


