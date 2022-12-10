using System.Collections;
using System.Collections.Generic;
using Unity.VisualScripting;
using UnityEngine;

[RequireComponent(typeof(Rigidbody2D))]
public class PlayerController : MonoBehaviour
{
    public bool HasAuthority = false;
    public GameObject[] weaponList;
    public WeaponController currWeaponController;
    public float speedMultiplier=10f;
    private Rigidbody2D rb;
    private Vector2 CurrentSpeed;
    // Start is called before the first frame update
    void Start()
    {
        weaponList = Resources.LoadAll<GameObject>("Weapons");
        rb = GetComponent<Rigidbody2D>();
        
        if(!HasAuthority){
            gameObject.AddComponent<PlayerPacketHandler>();
        }
        
        SwitchToWeapon(0);

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
            NetworkManager.instance.SendAction(s); 
        }
    }
}

