using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerPacketHandler : PacketHandler
{

    public bool hasAuthority=false;
    private PlayerInfo pState;
    void Update()
    {
        if (hasAuthority) //send update packets to server only if object has authority
        {
            pState = new PlayerInfo();
            pState.loadFromTransform(transform);
            NetworkManager.instance.SendState(pState);                
        }

    }
    
    
    // Start is called before the first frame update
    public virtual void HandleShoot(Shoot p)
    {
    
    }
    
    public virtual void HandlePStats(PlayerStats p)
    {

    }

}
