using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TargetGenerator : MonoBehaviour
{
    [SerializeField] private GameObject targetPrefab;
    [SerializeField] Camera mainCamera;
    private  int screenWidth, screenHeight;
    private float screenWidthMargin, screenHeightMargin;
    // Start is called before the first frame update
    void Start()
    {
        screenWidth = Screen.width;
        screenWidthMargin = screenWidth*0.05f;
        screenHeight = Screen.height;
        screenHeightMargin = screenHeight*0.05f;
    }

    // Update is called once per frame
    void Update()
    {

    }

    public void generate()
    {
        Vector3 randomPos = mainCamera.ScreenToWorldPoint(
            new Vector3(Random.Range(screenWidthMargin, screenWidth - screenWidthMargin),
                        Random.Range(screenHeightMargin, screenHeight - screenHeightMargin), 9f));
        GameObject target = Instantiate(targetPrefab, randomPos, new Quaternion(0, 0, 0, 0)) as GameObject;
        TargetController targetController = target.GetComponent<TargetController>();
        targetController.initialize(100, 3.0f);
    }
}
