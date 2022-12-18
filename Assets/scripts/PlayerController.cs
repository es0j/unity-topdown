using System.Collections;
using System.Collections.Generic;
using Unity.VisualScripting;
using UnityEngine;

[RequireComponent(typeof(PlayerPacketHandler))]
[RequireComponent(typeof(Rigidbody2D))]
public class PlayerController : MonoBehaviour
{
    public bool HasAuthority = false;
    public GameObject[] weaponList;
    public WeaponController currWeaponController;
    public float speedMultiplier=10f;
    private Rigidbody2D rb;
    private Vector2 CurrentSpeed;

    private Camera cameraComp;
    // Start is called before the first frame update
    void Start()
    {
        weaponList = Resources.LoadAll<GameObject>("Weapons");
        rb = GetComponent<Rigidbody2D>();
        SwitchToWeapon(0);
        if (HasAuthority)
        {
            
        }
        else
        {
            rb.isKinematic  = true;
        }
        

    }
    public void MoveHorizontal(float input)
    {
        
    }

    public void MoveVertical(float input)
    {
        
    }
    public void SwitchToWeapon(uint weaponId){
        //spawn weapon attatched
        GameObject spawnedWeapon =  Instantiate(weaponList[weaponId],transform);
        currWeaponController = spawnedWeapon.GetComponent<WeaponController>();
    }
    

    // Update is called once per frame
    void Update()
    {
        if (!HasAuthority)
        {
            return;
        }
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
            if(currWeaponController.ShootWeapon()){
                ReplicateShoot();
            }
        }

        rb.MovePosition(rb.position +  CurrentSpeed * Time.fixedDeltaTime * speedMultiplier);    
       
        
        Vector3 worldPosition = Camera.main.ScreenToWorldPoint(Input.mousePosition);
        
        var dir = worldPosition - transform.position;
        var angle = Mathf.Atan2(dir.y, dir.x) * Mathf.Rad2Deg;
        transform.rotation = Quaternion.AngleAxis(angle, Vector3.forward);

        ReplicatePosition();

        
        
    }


    void ReplicatePosition(){
        if(HasAuthority){
            PlayerInfo pState;
            pState = new PlayerInfo();
            pState.loadFromTransform(transform);
            NetworkManager.instance.SendState(pState);    
        }
    }
    void ReplicateShoot(){
        if(HasAuthority){
            Shoot s = new Shoot();

            Transform weaponMuzzleTransform = currWeaponController.GetWeaponEndpoint();
            
            s.start_x = weaponMuzzleTransform.position.x;
            s.start_y = weaponMuzzleTransform.position.y;
            Vector3 end = weaponMuzzleTransform.position + (weaponMuzzleTransform.right * 100.0f);
            
            s.end_x = end.x;
            s.end_y = end.y;

            Vector3 startDraw = new Vector3(s.start_x, s.start_y, 20);
            Vector3 endDraw = new Vector3(end.x, end.y, 20);
            
            Debug.DrawLine(startDraw, endDraw, Color.red, 200.5f,false);
            NetworkManager.instance.SendAction(s); 
            
        }
    }
}

