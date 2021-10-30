import cv2
import numpy as np
import time
from pprint import pprint as pp
import socket
import json

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

    def setCfgValue(self, name):

        windowName = str(name)
        self.h_min = cv2.getTrackbarPos("H_min", windowName)
        self.h_max = cv2.getTrackbarPos("H_max", windowName)
        self.v_min = cv2.getTrackbarPos("V_min", windowName)
        self.v_max = cv2.getTrackbarPos("V_max", windowName)
        self.s_min = cv2.getTrackbarPos("S_min", windowName)
        self.s_max = cv2.getTrackbarPos("S_max", windowName)

class FrameCaptureFailed(Exception):
    def __init__(self):
        pass
    def __str__(self):
        return "Captureing Frame Failed!"

class CornersNotFound(Exception):
    def __init__(self):
        pass
    def __str__(self):
        return "corner markers are not found"

#udpサーバのアドレス
serv_addr=('127.0.0.1',2323)
cap = None
config_red = ColorConfig()
config_green = ColorConfig()
RED_WINDOW_NAME = "config_red"
GREEN_WINDOW_NAME = "config_green"
image_width = None
image_height = None
parse_matrix = None
client = None
filledImg = None
KEY_ESC = 27
CAMERA = 0
DO_MONITOR = True
LASER_SIZE = 4
poly_centors = []
poly_cp_frame = None


def pass_(*args, **kwargs):
    pass

def draw_mark(event, x, y, flags, params):
    global poly_centors
    global poly_cp_frame
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.drawMarker(poly_cp_frame, (x, y), (50,50, 255),markerSize=10)
        poly_centors.append((x,y))

def makePolyMask():
    global poly_centors
    global poly_cp_frame
    try:
        ret,frame = cap.read()
        if (frame is None) or (frame.size == 0):
            print("Broken Image")
            return np.full((image_height, image_width, 1), 255, dtype=np.uint8)
        poly_cp_frame = frame.copy()
        mask_zero = np.full((int(image_height), int(image_width), 1), 0, dtype=np.uint8)
        cp_mask_poly = mask_zero.copy()
        poly_centors = []
        cv2.namedWindow("polymask")
        cv2.setMouseCallback("polymask",draw_mark)
        while True:
            cv2.imshow("polymask",poly_cp_frame)
            key = cv2.waitKey(1)
            if key == KEY_ESC:
                break
            elif key == ord('q'):
                poly_centors = []
                ret,frame = cap.read()
                if (frame is None) or (frame.size == 0):
                    print("Broken Image")
                poly_cp_frame = frame.copy()
                cp_mask_poly = mask_zero.copy()
            elif key == ord('e'):
                poly_centors = []
            elif key == ord('a'):
                print(poly_centors)
                if len(poly_centors) < 2:
                    print("marker are too few")
                    continue
                points = np.array(poly_centors)
                cv2.fillConvexPoly(poly_cp_frame, points, (255, 255, 0))
                cv2.fillConvexPoly(cp_mask_poly, points, 255)
        cv2.destroyAllWindows()
        return cp_mask_poly
    except (KeyboardInterrupt, SystemExit):
        return np.full((image_height, image_width, 1), 255, dtype=np.uint8)

def createCfgWindow(name):
    """色の範囲設定用ウィンドウの作成"""
    #TODO リアルタイムでの色設定変更対応
    windowName = str(name)
    cv2.namedWindow(windowName)
    cv2.createTrackbar("H_min", windowName, 0, 179, pass_)# Hueの最大値は179
    cv2.createTrackbar("H_max", windowName, 179, 179, pass_)
    cv2.createTrackbar("S_min", windowName, 0, 255, pass_)
    cv2.createTrackbar("S_max", windowName, 255, 255, pass_)
    cv2.createTrackbar("V_min", windowName, 0, 255, pass_)
    cv2.createTrackbar("V_max", windowName, 255, 255, pass_)

def cvtMaskedImage(frame, cc, poly_mask):
    """設定値からマスク後のイメージを生成"""
    #TODO 取り込み範囲指定マスクの作成
    hsv_img =  cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
    mask_img = cv2.inRange(hsv_img, cc.getMin(), cc.getMax())
    mask_img = cv2.bitwise_and(mask_img, mask_img, mask=poly_mask)
    result_img = cv2.bitwise_and(hsv_img, hsv_img, mask=mask_img)
    result_img = cv2.cvtColor(result_img, cv2.COLOR_HSV2RGB)
    result_img = cv2.GaussianBlur(result_img, (3,3), 1)
    #mask_img = cv2.GaussianBlur(mask_img, (2,2), 1)
    return result_img, mask_img


def colorConfigure(cc, windowName, cap, poly_mask):
    """色設定"""

    createCfgWindow(windowName)
    while not cc.updated:
        ret,frame = cap.read()
        if  (frame is None) or (frame.size == 0):
            raise FrameCaptureFailed

        cc.setCfgValue(windowName)
        result_img, _ = cvtMaskedImage(frame, cc, poly_mask)
        cv2.imshow(windowName, result_img)

        key = cv2.waitKey(1)
        if key == ord('a'):
            cc.updated = True
            pp(vars(cc))
            cv2.destroyAllWindows()

def getConnectedComponents(img):
    """背景を除いたコンポーネント検出"""
    num_labels, _, stats, centers = cv2.connectedComponentsWithStats(img)
    num_labels = num_labels - 1
    stats = np.delete(stats, 0, 0)
    centers = np.delete(centers, 0, 0)
    return num_labels, stats, centers

def getMatrix(cc,cap, poly_mask):
    """四隅のマーカーを用いた補正値算出"""
    global image_width,image_height

    ret, frame = cap.read()
    if(frame is None) or (frame.size == 0):
        raise FrameCaptureFailed
    result_img, mask_img = cvtMaskedImage(frame, cc, poly_mask)
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
            if key == ord('a'):
                cv2.destroyAllWindows()
                break
            elif key == ord('q'):
                cc.updated = False
                cv2.destroyAllWindows()
                return -1, 0, 0

        image_center_x = sum(c[0] for c in centers)/4
        image_center_y = sum(c[1] for c in centers)/4
        LEFT = UPPER = True
        RIGHT = LOWER = False
        corners = {(c[0] < image_center_x, c[1] < image_center_y):c for c in centers}

        if len(corners) < 4:
            print (corners)
            print("corner_markers are invalid.")
            cc.updated = False
            return -1, 0, 0

        src_corner = np.float32([corners[(LEFT,UPPER)], corners[(RIGHT,UPPER)], corners[(LEFT,LOWER)], corners[(RIGHT,LOWER)]])
        print(src_corner)
        dst_corner = np.float32([[0,0],[image_width,0],[0,image_height],[image_width,image_height]])
        print("↓")
        print(dst_corner)
        matrix = cv2.getPerspectiveTransform(src_corner,dst_corner)
        print(matrix)
        return 0, matrix, src_corner

def getCenter(img):
    """赤点の重心算出"""
    num_labels, stats, centers = getConnectedComponents(img)

    if num_labels < 1 or stats[0,4] < LASER_SIZE:
        return np.float32([-1,-1])

    max_index = np.argmax(stats[:,4])
    x_target = int(centers[max_index][0])
    y_target = int(centers[max_index][1])

    return np.float32([x_target, y_target])

def fixCenter(center, src_corner, parse_matrix):
    """パース補正"""
    points = np.vstack([src_corner, center])
    out = cv2.perspectiveTransform(np.array([points]), parse_matrix)
    return out.astype(int)[:, 4][0], out.astype(int)[:, 0:4][0]

def sendUdp(center, corner):
    """中心座標のUDP送信"""
    #TODO 異常系の処理
    if corner[3][0] != image_width or corner[3][1] != image_height:
        print("[Warn]!!!The parse correction may have failed!!!")
        return -1

    if center[0] < 0 or image_width < center[0] or center[1] < 0 or image_height < center[1]:
        print("point isn't in range")
        return 1

    message = json.dumps({"x_target":str(center[0]/image_width), "y_target":str(center[1]/image_height)})
    client.sendto(message.encode("UTF-8"), serv_addr)
    print(message)
    return 0


def main() -> None:
    global cap
    global config_red
    global config_green
    global filledImg
    global image_width,image_height
    global parse_matrix
    global client

    cap = cv2.VideoCapture(CAMERA)
    image_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    image_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    if(DO_MONITOR):
        filledImg = np.full((int(image_height),int(image_width), 3), 200, dtype=np.uint8)
    poly_mask = makePolyMask()
    colorConfigure(config_red, RED_WINDOW_NAME, cap, poly_mask)
    st = -1
    while st != 0:
        colorConfigure(config_green, GREEN_WINDOW_NAME, cap, poly_mask)
        st, parse_matrix, src_corner = getMatrix(config_green, cap, poly_mask)

    try:
        while True:
            ret,frame = cap.read()
            if  (frame is None) or (frame.size == 0):
                print("Broken Image")
                continue
            _, masked_img = cvtMaskedImage(frame, config_red, poly_mask)
            center = getCenter(masked_img)
            center, corner= fixCenter(center, src_corner, parse_matrix)
            sendUdp(center, corner)
            if(DO_MONITOR):
                img_monitor = filledImg.copy()
                for p in corner:
                    cv2.circle(img_monitor, p, 10, (20,255,20), thickness=3)
                cv2.drawMarker(img_monitor, center, (50,50, 255),markerSize=10)
                cv2.imshow("watch", img_monitor)
                cv2.imshow("camera", frame)
                key = cv2.waitKey(1)
                if key == KEY_ESC:
                    break

    except(KeyboardInterrupt,SystemExit):
        print("exit")

if __name__ == "__main__":
    main()