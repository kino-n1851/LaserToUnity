using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BlueController : MonoBehaviour
{
    Transform mTransform;
    private Ray ray;
    private RaycastHit hit;
    private float x_target,y_target;
    private bool setPos = false;
    [SerializeField] Camera camera;

    // Start is called before the first frame update
    void Start()
    {
        mTransform = this.gameObject.GetComponent<Transform>();
    }

    // Update is called once per frame
    void Update()
    {
        if (Input.GetMouseButtonDown(0))
        {
            _raycast(Input.mousePosition);
            Debug.Log(Input.mousePosition);
        }
        if (setPos) 
        {
            _raycast(new Vector3(x_target, y_target, 0));
            setPos = false;
        }
    }

    public void moveBlue(float x, float y)
    {
        var worldPoint = Vector3.zero;
        ///RectTransformUtility.ScreenPointToWorldPointInRectangle(graphic.rectTransform, screenPoint, camera, out worldPoint);

    }

    public void _raycast(Vector3 pos)
    {
        ray = camera.ScreenPointToRay(pos);
        Debug.DrawRay(ray.origin, ray.direction * 1000, Color.cyan, 0.1f, false);
        if (Physics.Raycast(ray, out hit, 10000000))
        {
            this.transform.position = new Vector3(hit.point.x, hit.point.y, 1);
        }
    }

    public void setPosion(float x, float y) 
    {
        x_target = x;
        y_target = y;
        setPos = true;
    }
}
