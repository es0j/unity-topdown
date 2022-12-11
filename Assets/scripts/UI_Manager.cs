using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

public class UI_Manager : MonoBehaviour
{
    
    #region Singleton
    public static UI_Manager instance=null;
    void Awake()
    {
        if (instance != null)
        {
            Debug.LogWarning("more than one instance on UI_Manager");
            return;
        }
        instance = this;
    }
    #endregion

    
    public GameObject  lifeText;
    // Start is called before the first frame update
    public void UpdateLifeDisplay(float newLife)
    {
        lifeText.GetComponent<TextMeshProUGUI>().text = newLife.ToString();
    }
}
