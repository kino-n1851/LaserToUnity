using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class RedController : MonoBehaviour {
    private Transform transform;
    public float moveSpeed = 0.3f;

    // Start is called before the first frame update
    void Start()
    {
        transform = this.gameObject.GetComponent <Transform>();
    }

    // Update is called once per frame
    void Update()
    {
        if (Input.GetKey(KeyCode.W)&&Input.GetKeyDown(KeyCode.D)){
            transform.position += new Vector3(Mathf.Sqrt(2), Mathf.Sqrt(2),0)*moveSpeed;
        }
        else if (Input.GetKey(KeyCode.W) && Input.GetKeyDown(KeyCode.A)){ 
            transform.position += new Vector3(-Mathf.Sqrt(2), Mathf.Sqrt(2), 0) * moveSpeed;
        }
        else if (Input.GetKey(KeyCode.S) && Input.GetKeyDown(KeyCode.D))
        {
            transform.position += new Vector3(Mathf.Sqrt(2), -Mathf.Sqrt(2), 0) * moveSpeed;
        }
        else if (Input.GetKey(KeyCode.S) && Input.GetKeyDown(KeyCode.A))
        {
            transform.position += new Vector3(-Mathf.Sqrt(2), -Mathf.Sqrt(2), 0) * moveSpeed;
        }
        else {
            if (Input.GetKey(KeyCode.W)){
                transform.position += new Vector3(0, 1, 0) * moveSpeed;
            }
            if (Input.GetKey(KeyCode.D)){
                transform.position += new Vector3(1, 0, 0) * moveSpeed;
            }
            if (Input.GetKey(KeyCode.S)){
                transform.position += new Vector3(0, -1, 0) * moveSpeed;
            }
            if (Input.GetKey(KeyCode.A)){
                transform.position += new Vector3(-1, 0, 0) * moveSpeed;
            }
        }

    }
}
