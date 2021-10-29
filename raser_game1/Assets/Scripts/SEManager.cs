using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SEManager : MonoBehaviour
{
    [SerializeField] AudioClip start;
    [SerializeField] AudioClip end;
    [SerializeField] AudioClip hit;
    [SerializeField] AudioClip buzzer;

    [SerializeField] GameObject audioObject;
    private AudioSource audioSource;
    // Start is called before the first frame update
    void Start()
    {
        audioSource = audioObject.GetComponent<AudioSource>();
    }

    // Update is called once per frame
    void Update()
    {
        
    }
    public void playSE(string name)
    {
        switch(name)
        {
            case "start":
                audioSource.PlayOneShot(start);
                break;

            case "hit":
                audioSource.PlayOneShot(hit);
                break;

            case "end":
                audioSource.PlayOneShot(end);
                break;

            case "buzzer":
                audioSource.PlayOneShot(buzzer);
                break;
        }
    }
}
