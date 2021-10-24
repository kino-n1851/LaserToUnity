using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TimeManager : MonoBehaviour
{
    private float time = 0;
    private float beforeTime = 0;
    float interval = 2.0f;
    private int fullTime = 100;
    private bool isStarted = true;
    private bool isFinished = false;
    private TargetGenerator targetGenerator;
    // Start is called before the first frame update
    void Start()
    {
        targetGenerator = GameObject.Find("TargetGenerator").GetComponent<TargetGenerator>();
        Debug.Log(targetGenerator);
    }

    // Update is called once per frame
    void Update()
    {
        if (!isStarted)return;
        if(isFinished)return;
        time += Time.deltaTime;
        if((time - beforeTime) >= interval)
        {
            beforeTime = time;
            targetGenerator.generate();
        }

        if (time > fullTime)isFinished = true;
    }
}
