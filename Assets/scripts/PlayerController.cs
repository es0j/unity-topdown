using System.Collections;
using System.Collections.Generic;
using Unity.VisualScripting;
using UnityEngine;

[RequireComponent(typeof(Rigidbody2D))]
public class PlayerController : MonoBehaviour
{
    public WeaponController currWeapon;
    public float speedMultiplier=10f;
    private Rigidbody2D rb;
    private Vector2 CurrentSpeed;
    // Start is called before the first frame update
    void Start()
    {
        rb = GetComponent<Rigidbody2D>();
    }
    public void MoveHorizontal(float input)
    {
        
    }

    public void MoveVertical(float input)
    {
        
    }
    

    // Update is called once per frame
    void Update()
    {
        CurrentSpeed = Vector2.zero;
        
        if (Input.GetKey(KeyCode.W))
        {
            CurrentSpeed.y = 1;
        }
        if (Input.GetKey(KeyCode.S))
        {
            CurrentSpeed.y = -1;
        }
        if (Input.GetKey(KeyCode.A))
        {
            CurrentSpeed.x = -1;
        }
        if (Input.GetKey(KeyCode.D))
        {
            CurrentSpeed.x = 1;
        }

        if (Input.GetMouseButtonDown(0) )
        {
            currWeapon.ShootWeapon();
        }

        rb.MovePosition(rb.position +  CurrentSpeed * Time.fixedDeltaTime * speedMultiplier);    
       
        
        Vector3 worldPosition = Camera.main.ScreenToWorldPoint(Input.mousePosition);
        
        var dir = worldPosition - transform.position;
        var angle = Mathf.Atan2(dir.y, dir.x) * Mathf.Rad2Deg;
        transform.rotation = Quaternion.AngleAxis(angle, Vector3.forward);
        
        
    }
}

