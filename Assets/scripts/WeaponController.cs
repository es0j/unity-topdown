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

    public IEnumerator StartCountdown(float countdownValue)
    {
        yield return new WaitForSeconds(countdownValue);
        isInCooldown = false;
    }
}
