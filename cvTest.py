import cv2
import numpy as np

def draw_mark(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.drawMarker(drawn_img, (x, y), (50,50, 255),markerSize=10)
        centors.append((x,y))

KEY_ESC = 27
filled_img = np.full((450 ,800 , 3), 200, dtype=np.uint8)
mask_img = np.full((450, 800, 1),0, dtype=np.uint8)
centors = []
cv2.namedWindow("test")
cv2.setMouseCallback("test",draw_mark)
drawn_img = filled_img.copy()
polymask_img = mask_img.copy()
try:
    while True:
        cv2.imshow("test",drawn_img)
        key = cv2.waitKey(1)
        if key == KEY_ESC:
            break
        elif key == ord('q'):
            centors = []
            drawn_img = filled_img.copy()
            polymask_img = mask_img.copy()
        elif key == ord('e'):
            centors = []
        elif key == ord('a'):
            print(centors)
            points = np.array(centors)
            cv2.fillConvexPoly(drawn_img, points, (255, 255, 0))
            cv2.fillConvexPoly(polymask_img, points, 255)
            cv2.imshow("mask",polymask_img)
except (KeyboardInterrupt, SystemExit):
    pass