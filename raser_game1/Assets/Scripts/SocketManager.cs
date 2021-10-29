using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using System.Text;
using UnityEngine.UI;

public class SocketManager : MonoBehaviour
{
    static private int unityPort = 2323;


    UDPServer UdpServ;
    private void ReceiveUdp(string msg) {
        ///Debug.Log(msg);
    }
    // Start is called before the first frame update
    void Start()
    {
        UdpServ = new UDPServer(unityPort);
        UdpServ.Received += ReceiveUdp;
        UdpServ.ListenStart();
    }

    // Update is called once per frame
    void Update()
    {

    }

    void OnApplicationQuit()
    {
        UdpServ.Dispose();
        Debug.Log("aaa");
    }

    public void dispose()
    {
        UdpServ.Dispose();
    }
}

public class UDPServer
{
    public delegate void ReceivedHandler(string strMsg);
    public ReceivedHandler Received;
    private Thread thread;
    private int nListenPort;
    private UdpClient client;
    private UdpPosition udpPosition;
    private int gameViewWidth, gameViewHeight;
    private HitManager hitManager;

    public UDPServer(int port = 20000)
    {
        nListenPort = port;
        client = null;
    }

    public void ListenStart()
    {
        hitManager = GameObject.Find("HitManager").GetComponent<HitManager>();
        gameViewHeight = Screen.height;
        gameViewWidth = Screen.width;
        Debug.Log(gameViewHeight);
        Debug.Log(gameViewWidth);
        client = new UdpClient(nListenPort);
        //client.ExclusiveAddressUse = true;
        //client.Connect("127.0.0.1",nListenPort);
        //client.ExclusiveAddressUse = true;
        thread = new Thread(new ThreadStart(Thread));
        thread.Start();
        Debug.Log("UDP Receive thread start");
    }

    public void Dispose()
    {
        if (thread != null)
        {
            thread.Abort();
            thread = null;
        }
        if (client != null)
        {
            client.Close();
            client.Dispose();
            client = null;
        }
    }

    private void Thread()
    {
        while (true)
        {
            if (client != null)
            {
                try
                {
                    IPEndPoint ep = null;
                    byte[] rcvBytes = client.Receive(ref ep);
                    string rcvMsg = string.Empty;
                    rcvMsg = System.Text.Encoding.UTF8.GetString(rcvBytes);
                    if (rcvMsg != string.Empty)
                    {
                        //Debug.Log("UDP受信メッセージ : " + rcvMsg);
                        udpPosition = JsonUtility.FromJson<UdpPosition>(rcvMsg);
                        hitManager.setPosion(udpPosition.x_target*gameViewWidth, udpPosition.y_target*-gameViewHeight + gameViewHeight);
                        Received?.Invoke(rcvMsg);
                    }
                }
                catch (System.Exception e)
                {
                    Debug.Log(e.Message);
                }
            }
            else
            {
                Debug.Log("Error:client = null");
            }
        }
    }

}
class UdpPosition
{
    public float x_target;
    public float y_target;
}
