using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class followerCam : MonoBehaviour
{
    // Start is called before the first frame update
    public GameObject target;

    // Update is called once per frame
    void Update()
    {
        if (target)
        {
            transform.position = new Vector3(target.transform.position.x,
                target.transform.position.y,
                transform.position.z);            
        }
        

    }
}
