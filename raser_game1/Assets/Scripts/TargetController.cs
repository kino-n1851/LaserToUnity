using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TargetController : MonoBehaviour
{
    private int myScore = 0;
    private float activeTime = 0;
    private bool active = false;
    private float duration = 1;
    [SerializeField] GameObject target;
    private float scoreTime = 0.3f;
    private float perfectTime = 3.0f;
    private GameObject scoreObject = null;
    private ScoreManager scoreManager = null;
    private TargetGenerator targetGenerator = null;
    private SEManager seManager = null;
    private TimeManager timeManager = null;
    private Rigidbody body = null;
    private float Acceleration = 1.0f;
    private int GOODSCORE = 125;
    private int PERFECTSCORE = 200;
    private float goodness = 0.0f;
    private float DIFFICULTY = 1.25f;
    private int combo;

    [SerializeField] GameObject laserHit;

    // Start is called before the first frame update
    void Start()
    {
        scoreObject = GameObject.Find("Score");
        scoreManager = scoreObject.GetComponent<ScoreManager>();
        targetGenerator = GameObject.Find("TargetGenerator").GetComponent<TargetGenerator>();
        seManager = GameObject.Find("SE").GetComponent<SEManager>();
        timeManager = GameObject.Find("TimeManager").GetComponent<TimeManager>();
        body = target.GetComponent<Rigidbody>();
    }

    // Update is called once per frame
    void Update()
    {
        if(!active)return;
        Acceleration = timeManager.getAccel();
        goodness = timeManager.getGood();
        combo = timeManager.getCombo();
        activeTime += Time.deltaTime;

        //if((activeTime - beforeTime) >= scoreTime)
        //{
        //    myScore -= 1;
        //    beforeTime = activeTime;
        //}

        if(activeTime > duration)
        {
            active = false;
            scoreManager.addResult("miss");
            seManager.playSE("buzzer");
            targetGenerator.decTarget();
            timeManager.setCombo(0);
            Destroy(target);
        }
    }

    public void initialize(float _duration){
        duration = _duration;
        active = true;
    }

    public void hit(){
        if(!active)return;
        Debug.Log("Hit");
        if(activeTime >= (perfectTime/(1 + (Acceleration - 1)*0.2f)))
        {
            //good
            seManager.playSE("hit");
            scoreManager.addResult("good");
            if(combo <= 10)scoreManager.getScore((int)(GOODSCORE * (1 + 0.05 * combo)));
            else scoreManager.getScore((int)(GOODSCORE * 2));
            timeManager.setGood(goodness + DIFFICULTY * 0.5f);
            timeManager.setAccel(Acceleration = 1 + goodness * 0.1f);
            active = false;
            GameObject effect = Instantiate(laserHit, target.transform.position, new Quaternion(0, 0, 0, 0)) as GameObject;
        }else
        {
            //perf
            seManager.playSE("hit");
            scoreManager.addResult("perfect");
            if (combo <= 10)scoreManager.getScore((int)(PERFECTSCORE * (1 + 0.05 * combo)));
            else scoreManager.getScore((int)(PERFECTSCORE * 2));
            timeManager.setGood(goodness + DIFFICULTY * 1);
            timeManager.setAccel(Acceleration = 1 + goodness * 0.1f);
            active = false;
            GameObject effect = Instantiate(laserHit, target.transform.position, new Quaternion(0, 0, 0, 0)) as GameObject;
        }
        timeManager.setCombo(combo + 1);

        targetGenerator.decTarget();
        Destroy(target);
    }
}
