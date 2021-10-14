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
ParseMatrix = None
client = None
filledImg = None
KEY_ESC = 27
CAMERA = 0
doWatch = True
laserSize = 2

def pass_(*args, **kwargs):
    pass

def init():
    #* 画像取り込みにおける初期設定
    global cap
    global imageWidth,imageHeight
    global client
    global filledImg

    cap = cv2.VideoCapture(CAMERA)
    imageWidth = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    imageHeight = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    if(doWatch):
        filledImg = np.full((int(imageHeight),int(imageWidth), 3), 200, dtype=np.uint8)

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
    #TODO 取り込み範囲指定マスクの作成
    hsv_img =  cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
    mask_img = cv2.inRange(hsv_img, cc.getMin(), cc.getMax())
    result_img = cv2.bitwise_and(hsv_img, hsv_img, mask=mask_img)
    result_img = cv2.cvtColor(result_img, cv2.COLOR_HSV2RGB)
    result_img = cv2.GaussianBlur(result_img, (3,3), 1)
    #mask_img = cv2.GaussianBlur(mask_img, (2,2), 1)
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

def getConnectedComponents(img):
    #* 背景を除いたコンポーネント検出
    num_labels, label, stats, centers = cv2.connectedComponentsWithStats(img)
    num_labels = num_labels - 1
    stats = np.delete(stats, 0, 0)
    centers = np.delete(centers, 0, 0)
    return num_labels, stats, centers

def getMatrix(cc,cap):
    #* 四隅のマーカーを用いた補正値算出
    global imageWidth,imageHeight

    ret, frame = cap.read()
    if(frame is None) or (frame.size == 0):
        return -1
    result_img, mask_img = cvtMaskedImage(frame, cc)
    num_labels, stats, centers = getConnectedComponents(mask_img)

    if num_labels >= 4:
        order = np.argsort(stats[:,4])[::-1]
        stats = stats[order][:4, :]
        centers = centers[order][:4, :]

        for stat in stats:
            result_img = cv2.rectangle(result_img, (stat[0],stat[1]), (stat[0]+stat[2],stat[1]+stat[3]), (255,50,50),2)

        while True:
            cv2.imshow("corner", result_img)
            key = cv2.waitKey(1)
            if key == KEY_ESC:
                cv2.destroyAllWindows()
                break

        image_center_x = 0
        image_center_y = 0
        for center in centers:
            image_center_x += center[0]
            image_center_y += center[1]
        image_center_x = image_center_x/4
        image_center_y = image_center_y/4
        print(image_center_x, image_center_y)

        corners = {}
        for center in centers:
            if center[0] < image_center_x and center[1] < image_center_y:
                corners["UL"] = center
            elif center[0] < image_center_x and center[1] > image_center_y:
                corners["LL"] = center
            elif center[0] > image_center_x and center[1] < image_center_y:
                corners["UR"] = center
            elif center[0] > image_center_x and center[1] > image_center_y:
                corners["LR"] = center
            else:
                raise ValueError("???")

        if len(corners) < 4:
            print (corners)
            print("corner_markers are invalid.")
            return -1

        src_corner = np.float32([corners["UL"], corners["UR"], corners["LL"], corners["LR"]])
        dst_corner = np.float32([[0,0],[imageWidth,0],[0,imageHeight],[imageWidth,imageHeight]])
        matrix = cv2.getPerspectiveTransform(src_corner,dst_corner)

        return matrix, src_corner

def getCenter(img):
    #* 赤点の重心算出
    num_labels, stats, centers = getConnectedComponents(img)

    if num_labels >= 1 and stats[0,4] > laserSize:
        max_index = np.argmax(stats[:,4])
        x_target = int(centers[max_index][0])
        y_target = int(centers[max_index][1])
    else:
        return np.float32([-1, -1])

    return np.float32([x_target, y_target])

def fixCenter(center, src_corner, parseMatrix):
    #* パース補正
    points = np.vstack([src_corner, center])
    out = cv2.perspectiveTransform(np.array([points]), parseMatrix)
    return out.astype(int)[:, 4][0], out.astype(int)[:, 0:4][0]

def sendUdp(center, corner):
    #* 中心座標のUDP送信
    if corner[3][0] != imageWidth or corner[3][1] != imageHeight:
        print("[Warn]!!!The parse correction may have failed!!!")
        return -1
    if center[0] < 0 or imageWidth < center[0] or center[1] < 0 or imageHeight < center[1]:
        print("point isn't in range")
        return 1
    message = json.dumps({"x_target":str(center[0]/imageWidth), "y_target":str(center[1]/imageHeight)})
    client.sendto(message.encode("UTF-8"), serv_addr)
    print(message)
    return 0


def main() -> None:
    global cap
    global config_red
    global config_green
    global filledImg

    init()
    colorConfigure(config_red, redWindowName, cap)
    colorConfigure(config_green, greenWindowName, cap)
    print("end")
    parseMatrix, src_corner= getMatrix(config_green, cap)
    try:
        while True:
            ret,frame = cap.read()
            if  (frame is None) or (frame.size == 0):
                print("Broken Image")
                continue
            _, masked_img = cvtMaskedImage(frame, config_red)
            center = getCenter(masked_img)
            center, corner= fixCenter(center, src_corner, parseMatrix)
            sendUdp(center, corner)
            if(doWatch):
                watchImg = filledImg.copy()
                for p in corner:
                    cv2.circle(watchImg, p, 10, (20,255,20), thickness=3)
                cv2.drawMarker(watchImg, center, (50,50, 255),markerSize=10)
                cv2.imshow("watch", watchImg)
                key = cv2.waitKey(1)
                if key == KEY_ESC:
                    break

    except(KeyboardInterrupt,SystemExit):
        print("exit")

if __name__ == "__main__":
    main()