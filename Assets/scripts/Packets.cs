using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Newtonsoft.Json;

public enum PcktType
{
    Error = 0,
    ClientHello,
    ServerHello,
    PlayerInfo,
    PlayerEnter,
    PlayerLeave,
    PlayerStats,
    Attack,
    Shoot
}

public class Packet
{
    public PcktType type;
    public int id;
    public string ToJson(int netId)
    {
        id = netId;
        return JsonConvert.SerializeObject(this);
    }
}

public class ClientHello : Packet
{
    public ClientHello()
    {
        type = PcktType.ClientHello;
    }
}

public class ServerHello : Packet
{
    public ServerHello()
    {
        type = PcktType.ServerHello;
    }
}

public class PlayerInfo : Packet
{
    public PlayerInfo()
    {
        type = PcktType.PlayerInfo;
    }
    //public Position position;
    public float x, y, rotation;
    public void loadFromTransform(Transform t)
    {
        x = t.position.x;
        y = t.position.y;
        rotation = t.rotation.z;
    }
}


public class PlayerEnter : Packet
{
    public PlayerEnter()
    {
        type = PcktType.PlayerEnter;
    }
    public int gid;
}

public class PlayerLeave : Packet
{
    public PlayerLeave()
    {
        type = PcktType.PlayerLeave;
    }

}

public class Shoot : Packet
{
    public float start_x, start_y, end_x, end_y;
    public Shoot()
    {
        type = PcktType.Shoot;
    }
}

public class PlayerStats : Packet
{
    public PlayerStats()
    {
        type = PcktType.PlayerStats;
    }
    public float health;
}
