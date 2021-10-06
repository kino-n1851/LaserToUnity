import cv2
import numpy as np
import time
from pprint import pprint as pp
import socket
import json

class ColorConfig:
    
    def __init__(self):
        self.h_min = 0
        self.h_max = 179
        self.s_min = 0
        self.s_max = 255
        self.v_min = 0
        self.v_max = 255


#udpサーバのアドレス
serv_addr=('127.0.0.1',2323)
cap = None
config_red = ColorConfig()
config_green = ColorConfig()

def pass_(*args, **kwargs):
        pass

def init():
    global cap

    cap = cv2.VideoCapture(2)
    imageWidth = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    imageHeight = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    

def colorConfigure():
    global cap
    global config_red
    global config_green
    isSetRed = False
    isSetGreen = False

    cv2.namedWindow("config_red")
    cv2.createTrackbar("H_min", "config_red", 0, 179, pass_)       # Hueの最大値は179
    cv2.createTrackbar("H_max", "config_red", 128, 179, pass_)
    cv2.createTrackbar("S_min", "config_red", 128, 255, pass_)
    cv2.createTrackbar("S_max", "config_red", 255, 255, pass_)
    cv2.createTrackbar("V_min", "config_red", 128, 255, pass_)
    cv2.createTrackbar("V_max", "config_red", 255, 255, pass_)

    while not isSetRed:
        ret,frame = cap.read()
        if  (frame is None) or (frame.size == 0):
            return -1
        config_red.h_min = cv2.getTrackbarPos("H_min", "config_red")
        config_red.h_max = cv2.getTrackbarPos("H_max", "config_red")
        config_red.s_min = cv2.getTrackbarPos("S_min", "config_red")
        config_red.s_max = cv2.getTrackbarPos("S_max", "config_red")
        config_red.v_min = cv2.getTrackbarPos("V_min", "config_red")
        config_red.v_max = cv2.getTrackbarPos("V_max", "config_red")
        hsv_img =  cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
        mask_img = cv2.inRange(hsv_img, (h_min_red, s_min_red, v_min_red, v_max_red), (h_max_red, s_max_red, v_max_red))
        result_img = cv2.bitwise_and(hsv_img, hsv_img, mask=mask_img)
        result_img = cv2.cvtColor(result_img, cv2.COLOR_HSV2RGB)
        result_img = cv2.GaussianBlur(result_img,(3,3),1)
        cv2.imshow("config_red", result_img)
        key = cv2.waitKey(1)
        if key == 27:                   # k が27(ESC)だったらwhileループを脱出，プログラム終了
            isSetRed = True
            cv2.destroyAllWindows()
    
    cv2.namedWindow("config_green")
    cv2.createTrackbar("H_min", "config_green", 0, 179, pass_)       # Hueの最大値は179
    cv2.createTrackbar("H_max", "config_green", 128, 179, pass_)
    cv2.createTrackbar("S_min", "config_green", 128, 255, pass_)
    cv2.createTrackbar("S_max", "config_green", 255, 255, pass_)
    cv2.createTrackbar("V_min", "config_green", 128, 255, pass_)
    cv2.createTrackbar("V_max", "config_green", 255, 255, pass_)

    while not isSetGreen:
        ret,frame = cap.read()
        if  (frame is None) or (frame.size == 0):
            return -1
        h_min_red = cv2.getTrackbarPos("H_min", "config_green")
        h_max_red = cv2.getTrackbarPos("H_max", "config_green")
        s_min_red = cv2.getTrackbarPos("S_min", "config_green")
        s_max_red = cv2.getTrackbarPos("S_max", "config_green")
        v_min_red = cv2.getTrackbarPos("V_min", "config_green")
        v_max_red = cv2.getTrackbarPos("V_max", "config_green")
        hsv_img =  cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
        mask_img = cv2.inRange(hsv_img, (h_min_red, s_min_red, v_min_red, v_max_red), (h_max_red, s_max_red, v_max_red))
        result_img = cv2.bitwise_and(hsv_img, hsv_img, mask=mask_img)
        result_img = cv2.cvtColor(result_img, cv2.COLOR_HSV2RGB)
        result_img = cv2.GaussianBlur(result_img,(3,3),1)
        cv2.imshow("config_green", result_img)
        key = cv2.waitKey(1)
        if key == 27:                   # k が27(ESC)だったらwhileループを脱出，プログラム終了
            isSetGreen = True
            cv2.destroyAllWindows()
    
    
def main() -> None:

    init()
    colorConfigure()
    print("end")

if __name__ == "__main__":
    main()