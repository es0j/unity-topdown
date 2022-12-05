using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;



public class PlayerReplicator : MonoBehaviour
{
    private PlayerInfo pState;
    // Update is called once per frame
    void Update()
    {
        
        pState = new PlayerInfo();
        pState.loadFromTransform(transform);
        NetworkManager.instance.SendState(pState);    

    }
    
}

