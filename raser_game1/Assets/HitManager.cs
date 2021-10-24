using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class HitManager : MonoBehaviour
{
    Transform mTransform;
    private Ray ray;
    private RaycastHit hit;
    private float x_target, y_target;
    private bool setPos = false;
    [SerializeField] Camera mainCamera;
    [SerializeField] GameObject dotPrefab;
    private float duration = 0.3f;

    // Start is called before the first frame update
    void Start()
    {
        mTransform = this.gameObject.GetComponent<Transform>();
    }

    // Update is called once per frame
    void Update()
    {
        if (setPos)
        {
            _raycast(new Vector3(x_target, y_target, 0));
            setPos = false;
        }
    }
    public void _raycast(Vector3 pos)
    {
        ray = mainCamera.ScreenPointToRay(pos);
        Debug.DrawRay(ray.origin, ray.direction * 1000, Color.cyan, 0.1f, false);
        if (Physics.Raycast(ray, out hit, 10000000))
        {
            GameObject dot = Instantiate(dotPrefab, new Vector3(hit.point.x, hit.point.y, 1), new Quaternion(0, 0, 0, 0)) as GameObject;
            DotController dotController = dot.GetComponent<DotController>();
            dotController.setDuration(duration);
            Debug.Log(hit.collider.gameObject);
            if (hit.collider.CompareTag("Target"))
            {
                Debug.Log(hit.collider.gameObject);
                TargetController targetController = hit.collider.gameObject.GetComponent<TargetController>();
                targetController.hit();
            }
        }
    }


    public void setPosion(float x, float y)
    {
        x_target = x;
        y_target = y;
        setPos = true;
    }
}
