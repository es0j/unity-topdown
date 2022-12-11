using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(PlayerController))]
public class PlayerPacketHandler : PacketHandler
{
    private PlayerController pController;
    void Start(){
        pController = GetComponent<PlayerController>();
    }
    
    // Start is called before the first frame update
    public override void HandleShoot(Shoot p)
    {
        Debug.Log("Replicating weapon visuals");
        if (pController.currWeaponController)
        {
            pController.currWeaponController.ShootVisual();    
        }
        
    }
    
    public override void HandlePStats(PlayerStats p)
    {
        Debug.Log("Replicating weapon visuals");
        UI_Manager.instance.UpdateLifeDisplay(p.health);
    }

}
