using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerPacketHandler : PacketHandler
{
    private PlayerController pController;
    void Start(){
        pController = GetComponent<PlayerController>();
    } 
    
    // Start is called before the first frame update
    public virtual void HandleShoot(Shoot p)
    {
        pController.currWeaponController.ShootVisual();
    }
    
    public virtual void HandlePStats(PlayerStats p)
    {

    }

}
