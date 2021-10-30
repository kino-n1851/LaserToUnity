using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TimeManager : MonoBehaviour
{
    private float gameTime = 0;
    private float beforeTime = 0;
    float interval = 2.0f;
    private int fullTime = 60;
    private float firstWaitTime = 0;
    private int DISPLAYTIME = 4;
    private int DISPLAYINTERVAL = 3;
    private float Acceleration = 1.0f;
    private float goodness = 2.0f;

    private bool isStarted = false;
    private bool isFinished = false;
    private TargetGenerator targetGenerator;
    [SerializeField] GameObject scoreObject;
    [SerializeField] GameObject audioObject;
    private ScoreManager scoreManager;
    private SEManager seManager = null;
    private int[] random_root = {4, 3, 2, 1, 0, 0, -1, -2, -3};
    private float[] random_time = {0,0,0,0,0,0,0,0,0};
    private int random_time_ct = 0;
    private int combo = 0;
    private int MaxCombo = 0;
    // Start is called before the first frame update
    void Start()
    {
        scoreManager = scoreObject.GetComponent<ScoreManager>();
        targetGenerator = GameObject.Find("TargetGenerator").GetComponent<TargetGenerator>();
        seManager = audioObject.GetComponent<SEManager>();
        Debug.Log(targetGenerator);
        Random.InitState(System.DateTime.Now.Millisecond);
        for (int i = 0; i < 9; i++)
        {
            int j = Random.Range(0,9);
            int temp = random_root[i];
            random_root[i] = random_root[j];
            random_root[j] = temp;
        }
        for (int i = 0; i < 9; i++)
        {
            random_time[i] = 1.0f + 0.1f * random_root[i];
        }
        seManager.playSE("start");
    }

    // Update is called once per frame
    void Update()
    {
        if (!isStarted){
            firstWaitTime += Time.deltaTime;
            if(firstWaitTime > 3.0f)
            {
                isStarted = true;
                gameTime = 0;
            }
            return;
        }
        if(isFinished)return;
        gameTime += Time.deltaTime;

        if(random_time_ct >= 11)
        {
            for (int i = 0; i < 9; i++)
            {
                int j = Random.Range(0,9);
                int temp = random_root[i];
                random_root[i] = random_root[j];
                random_root[j] = temp;
            }
            for (int i = 0; i < 9; i++)
            {
                random_time[i] = 1.0f + 0.1f * random_root[i];
            }
            random_time_ct = 0;
        }

        if(((gameTime - beforeTime) * random_time[random_time_ct%9] * Acceleration) >= DISPLAYINTERVAL)
        {
            random_time_ct++;
            beforeTime = gameTime;
            targetGenerator.generate(DISPLAYTIME/(1 + (Acceleration - 1) * 0.2f));
        }
        if (gameTime > fullTime)
        {
            isFinished = true;
            seManager.playSE("end");
            scoreManager.finish();
        }
    }

    public float getAccel()
    {
        return Acceleration;
    }
    public float getGood()
    {
        return goodness;
    }
    public int getCombo()
    {
        return combo;
    }
    public void setAccel(float ac)
    {
        Acceleration = ac;
    }
    public void setGood(float go)
    {
        goodness = go;
    }
    public void setCombo(int co)
    {
        combo = co;
        if(combo >= MaxCombo)MaxCombo = combo;
    }
}
