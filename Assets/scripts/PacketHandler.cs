using System;
using System.IO;
using System.Net.Sockets;
using UnityEngine;
using System.Threading;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using Newtonsoft.Json;

public class PacketHandler : MonoBehaviour
{

    void OnDrawGizmos()
    {
        Gizmos.color = Color.red;
        Gizmos.DrawSphere(this.transform.position, 1.2f);
    }
    
    public void HandlePacket(PcktType pType, string newPacket)
    {
        switch (pType)
        {
            case PcktType.PlayerInfo:
                PlayerInfo pInfo = JsonConvert.DeserializeObject<PlayerInfo>(newPacket);
                HandlePInfo(pInfo);
                break;
            
            case PcktType.Shoot:
                Shoot shoot = JsonConvert.DeserializeObject<Shoot>(newPacket);
                HandleShoot(shoot);
                break;
            
            case PcktType.PlayerStats:
                PlayerStats pStats = JsonConvert.DeserializeObject<PlayerStats>(newPacket);
                HandlePStats(pStats);
                break;
            
            default:
                Debug.LogWarning("Unkonw packet recieved: "+newPacket);
                break;
        }
        
    }

    public virtual void HandlePInfo(PlayerInfo p)
    {
        Vector3 newPosition = new Vector3(p.x,p.y);
        transform.position = newPosition;
    }
    
    public virtual void HandleShoot(Shoot p)
    {

    }
    
    public virtual void HandlePStats(PlayerStats p)
    {

    }
    
    
}

