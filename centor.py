import cv2
import numpy as np
import time
from pprint import pprint as pp
import socket
import json

serv_addr=('127.0.0.1',2323)

def pass_(x):
        pass

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    cap = cv2.VideoCapture(0)
    imageWidth = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    imageHeight = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    cv2.namedWindow("OpenCV Window")
    cv2.createTrackbar("H_min", "OpenCV Window", 0, 179, pass_)       # Hueの最大値は179
    cv2.createTrackbar("H_max", "OpenCV Window", 128, 179, pass_)
    cv2.createTrackbar("S_min", "OpenCV Window", 128, 255, pass_)
    cv2.createTrackbar("S_max", "OpenCV Window", 255, 255, pass_)
    cv2.createTrackbar("V_min", "OpenCV Window", 128, 255, pass_)
    cv2.createTrackbar("V_max", "OpenCV Window", 255, 255, pass_)
    try:
        while True:
            ret,frame = cap.read()
            if  (frame is None) or (frame.size == 0):
                continue
            bgr_img = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            #bgr_img = cv2.resize(bgr_img, dsize=(800, 600))
            hsv_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2HSV)

            h_min = cv2.getTrackbarPos("H_min", "OpenCV Window")
            h_max = cv2.getTrackbarPos("H_max", "OpenCV Window")
            s_min = cv2.getTrackbarPos("S_min", "OpenCV Window")
            s_max = cv2.getTrackbarPos("S_max", "OpenCV Window")
            v_min = cv2.getTrackbarPos("V_min", "OpenCV Window")
            v_max = cv2.getTrackbarPos("V_max", "OpenCV Window")

            mask_img = cv2.inRange(hsv_img, (h_min, s_min, v_min), (h_max, s_max, v_max)) # HSV画像なのでタプルもHSV並び
            result_img = cv2.bitwise_and(hsv_img, hsv_img, mask=mask_img)
            result_img = cv2.cvtColor(result_img, cv2.COLOR_HSV2RGB)
            result_img = cv2.GaussianBlur(result_img,(3,3),1)
            label_img = result_img

            num_labels, label, stats, center = cv2.connectedComponentsWithStats(mask_img)
            num_labels = num_labels - 1
            stats = np.delete(stats, 0, 0)
            center = np.delete(center, 0, 0)
            pp(list(stats))
            pp(center)
            #time.sleep(0.01)

            if num_labels >= 1:
                # 面積最大のインデックスを取得
                max_index = np.argmax(stats[:,4])
                #print max_index

                # 面積最大のラベルのx,y,w,h,面積s,重心位置mx,myを得る
                x = stats[max_index][0]
                y = stats[max_index][1]
                w = stats[max_index][2]
                h = stats[max_index][3]
                s = stats[max_index][4]
                mx = int(center[max_index][0])
                my = int(center[max_index][1])
                #print("(x,y)=%d,%d (w,h)=%d,%d s=%d (mx,my)=%d,%d"%(x, y, w, h, s, mx, my) )

                # ラベルを囲うバウンディングボックスを描画
                cv2.rectangle(label_img, (x, y), (x+w, y+h), (255, 0, 255))

                # 重心位置の座標を表示
                cv2.putText(label_img, "%d,%d"%(mx,my), (x-15, y+h+15), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 0))
                cv2.putText(label_img, "%d"%(s), (x, y+h+15), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 0))
                message = json.dumps({"x_target":str(mx/imageWidth), "y_target":str(my/imageHeight)})
                client.sendto(message.encode("UTF-8"), serv_addr)
                print(message)
                
            
            cv2.imshow("OpenCV Window", result_img)
            key = cv2.waitKey(1)
            if key == 27:                   # k が27(ESC)だったらwhileループを脱出，プログラム終了
                break
            time.sleep(3)
    
    except(KeyboardInterrupt,SystemExit):
        print("exit")



if __name__ == "__main__":
    main()