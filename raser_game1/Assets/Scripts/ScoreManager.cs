using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class ScoreManager : MonoBehaviour
{
    [SerializeField] GameObject scoreObject;
    [SerializeField] GameObject finishObject;
    private int score = 0;
    private int combo = 0, miss = 0, good = 0, perfect = 0;
    private int maxCombo = 0;
    private Text scoreText = null;
    private Text finishScore = null;
    // Start is called before the first frame update
    void Start()
    {
        scoreText = scoreObject.GetComponent<Text>();
        finishScore = scoreObject.GetComponent<Text>();
        finishObject.SetActive(false);
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public void getScore(int _score)
    {
        score += _score;
        scoreText.text = "Score: " + score.ToString();
    }

    public void finish()
    {
        finishScore.text = "Score: " + score.ToString();
        finishObject.SetActive(true);
    }

    public void addResult(string name)
    {
        switch (name)
        {
            case "miss":
                miss += 1;
                break;
            
            case "good":
                good += 1;
                break;
            
            case "perfect":
                perfect += 1;
                break;

        }
    }
}
