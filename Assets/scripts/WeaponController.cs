using System.Collections;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;

public class WeaponController : MonoBehaviour
{
    public GameObject bulletType;
    public float cooldownTime=0.5f;
    private bool isInCooldown = false;
    public Vector3 spawnPosition;

    public bool ShootWeapon()
    {
        if (isInCooldown)
        {
            return false;
        }
        Transform bulletSpawnPoint = this.gameObject.transform.GetChild(0);
        Instantiate(bulletType,bulletSpawnPoint.position ,bulletSpawnPoint.rotation);
        isInCooldown = true;
        StartCoroutine(StartCountdown(cooldownTime));

        return true;
    }
    public void ShootVisual()
    {
        Debug.Log("Shooting!");
        Transform bulletSpawnPoint = this.gameObject.transform.GetChild(0);
            
        Instantiate(bulletType,bulletSpawnPoint.position ,bulletSpawnPoint.rotation);
        isInCooldown = true;
            
        StartCoroutine(StartCountdown(cooldownTime));
        
    }

    void OnDrawGizmos()
    {
        Transform t = GetWeaponEndpoint();
        //Gizmos.color = Color.red;
        
        
        Transform weaponMuzzleTransform = GetWeaponEndpoint();
            

        Vector3 end = weaponMuzzleTransform.position + (weaponMuzzleTransform.right * 100.0f);
        
        
        Gizmos.DrawLine(weaponMuzzleTransform.position,end);
        //Gizmos.DrawSphere(this.transform.position, 1.5f);
    }

    
    public Transform GetWeaponEndpoint()
    {
        return gameObject.transform.Find("SpawnPoint");
    }

    public IEnumerator StartCountdown(float countdownValue)
    {
        yield return new WaitForSeconds(countdownValue);
        isInCooldown = false;
    }
}
