using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class DotController : MonoBehaviour
{
    float passedTime = 0;
    float duration = 100.0f;
    [SerializeField] GameObject dot;
    private bool isDurationSet = false;
    // Start is called before the first frame update
    void Start()
    {

    }

    // Update is called once per frame
    void Update()
    {
        if (isDurationSet)
        {
            passedTime += Time.deltaTime;
            if (passedTime > duration)
            {
                Destroy(dot);
            }
        }
    }

    public void setDuration(float _duration) 
    {
        duration = _duration;
        isDurationSet = true;
    }
}
