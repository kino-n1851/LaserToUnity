import cv2
import numpy as np
import time
from pprint import pprint as pp
import socket
import json
import pprint

class ColorConfig:
    #* 色管理用クラスの定義
    def __init__(self):
        self.h_min = 0
        self.h_max = 179
        self.s_min = 0
        self.s_max = 255
        self.v_min = 0
        self.v_max = 255
        self.updated = False

    def getMin(self):
        return (self.h_min, self.s_min, self.v_min)

    def getMax(self):
        return (self.h_max, self.s_max, self.v_max)

#udpサーバのアドレス
serv_addr=('127.0.0.1',2323)
cap = None
config_red = ColorConfig()
config_green = ColorConfig()
redWindowName = "config_red"
greenWindowName = "config_green"
imageWidth = None
imageHeight = None
KEY_ESC = 27

def pass_(*args, **kwargs):
    pass

def init():
    #* 画像取り込みにおける初期設定
    global cap
    global imageWidth,imageHeight

    cap = cv2.VideoCapture(2)
    imageWidth = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    imageHeight = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

def createCfgWindow(name):
    #* 色の範囲設定用ウィンドウの作成
    windowName = str(name)
    cv2.namedWindow(windowName)
    cv2.createTrackbar("H_min", windowName, 0, 179, pass_)# Hueの最大値は179
    cv2.createTrackbar("H_max", windowName, 128, 179, pass_)
    cv2.createTrackbar("S_min", windowName, 128, 255, pass_)
    cv2.createTrackbar("S_max", windowName, 255, 255, pass_)
    cv2.createTrackbar("V_min", windowName, 128, 255, pass_)
    cv2.createTrackbar("V_max", windowName, 255, 255, pass_)

def setCfgValue(cc, name):
    #* トラックバー値の保存
    windowName = str(name)
    cc.h_min = cv2.getTrackbarPos("H_min", windowName)
    cc.h_max = cv2.getTrackbarPos("H_max", windowName)
    cc.v_min = cv2.getTrackbarPos("V_min", windowName)
    cc.v_max = cv2.getTrackbarPos("V_max", windowName)
    cc.s_min = cv2.getTrackbarPos("S_min", windowName)
    cc.s_max = cv2.getTrackbarPos("S_max", windowName)

def cvtMaskedImage(frame, cc):
    #* 設定値からマスク後のイメージを生成
    hsv_img =  cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
    mask_img = cv2.inRange(hsv_img, cc.getMin(), cc.getMax())
    result_img = cv2.bitwise_and(hsv_img, hsv_img, mask=mask_img)
    result_img = cv2.cvtColor(result_img, cv2.COLOR_HSV2RGB)
    result_img = cv2.GaussianBlur(result_img,(3,3),1)
    return result_img, mask_img


def colorConfigure(cc, windowName, cap):
    #* 色設定
    cc.updated = False

    createCfgWindow(windowName)
    while not cc.updated:
        ret,frame = cap.read()
        if  (frame is None) or (frame.size == 0):
            return -1

        setCfgValue(cc, windowName)
        result_img, _ = cvtMaskedImage(frame, cc)
        cv2.imshow(windowName, result_img)

        key = cv2.waitKey(1)
        if key == KEY_ESC:
            cc.updated = True
            pprint.pprint(vars(cc))
            cv2.destroyAllWindows()

def getMatrix(cc,cap):
    global imageWidth,imageHeight
    ret, frame = cap.read()
    if(frame is None) or (frame.size == 0):
        return -1
    result_img, mask_img = cvtMaskedImage(frame, cc)
    num_labels, label, stats, centers = cv2.connectedComponentsWithStats(mask_img)
    num_labels = num_labels - 1
    stats = np.delete(stats, 0, 0)
    centers = np.delete(centers, 0, 0)
    if num_labels >= 4:
        order = np.argsort(stats[:,4])[::-1]
        stats = stats[order][:4, :]
        centers = centers[order][:4, :]

        for stat in stats:
            result_img = cv2.rectangle(result_img, (stat[0],stat[1]), (stat[0]+stat[2],stat[1]+stat[3]), (255,50,50),2)
        key = cv2.waitKey(1)
        if key == KEY_ESC:
            cv2.destroyAllWindows()
        image_centor_x = 0
        image_centor_y = 0
        for center in centers:
            image_centor_x += center[0]
            image_centor_y += center[1]
        image_centor_x = image_centor_x/4
        image_centor_y = image_centor_y/4
        print(image_centor_x, image_centor_y)
        corners = {}
        for center in centers:
            if center[0] < image_centor_x and center[1] < image_centor_y:
                corners["UL"] = center
            elif center[0] < image_centor_x and center[1] > image_centor_y:
                corners["LL"] = center
            elif center[0] > image_centor_x and center[1] < image_centor_y:
                corners["UR"] = center
            elif center[0] > image_centor_x and center[1] > image_centor_y:
                corners["LR"] = center
            else:
                break
        if len(corners) < 4:
            print (corners)
            print("eee")
            return -1
        src_corner = np.float32([corners["UL"], corners["UR"], corners["LL"], corners["LR"]])
        dst_corner = np.float32([[0,0],[imageWidth,0],[0,imageHeight],[imageWidth,imageHeight]])
        matrix = cv2.getPerspectiveTransform(src_corner,dst_corner)
        print(src_corner.astype(int))
        out = cv2.perspectiveTransform(np.array([src_corner]),matrix)
        print(out.astype(int))
        #for arr in src_corner:
        #    arr = np.append(arr, 1)
        #    print(np.dot(matrix, arr).astype(int))


def main() -> None:
    global cap
    global config_red
    global config_green

    init()
    #colorConfigure(config_red, redWindowName, cap)
    colorConfigure(config_green, greenWindowName, cap)
    print("end")
    getMatrix(config_green, cap)

if __name__ == "__main__":
    main()