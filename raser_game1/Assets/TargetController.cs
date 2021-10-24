using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TargetController : MonoBehaviour
{
    private int myScore = 0;
    private float activeTime = 0;
    private bool active = false;
    private float duration = 1;
    private float beforeTime = 0;
    [SerializeField] GameObject target;
    private float scoreTime = 0.3f;

    // Start is called before the first frame update
    void Start()
    {
    }

    // Update is called once per frame
    void Update()
    {
        if(!active)return;
        activeTime += Time.deltaTime;

        if((activeTime - beforeTime) >= scoreTime)
        {
            myScore -= 1;
            beforeTime = activeTime;
        }

        if(activeTime > duration)
        {
            Destroy(target);
        }
    }

    public void initialize(int maxScore, float _duration){
        duration = _duration;
        myScore = maxScore;
        active = true;
    }

    public void hit(){
        Debug.Log("Hit");
        Debug.Log(myScore);
        Destroy(target);
    }
}
