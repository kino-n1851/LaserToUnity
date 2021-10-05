import cv2
import numpy as np
import random

def pass_(x):
  pass

img = cv2.imread('../daikei4.png')
y_img,x_img = img.shape[0], img.shape[1]
bgr_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
hsv_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2HSV)

cv2.namedWindow("OpenCV Window")
cv2.createTrackbar("H_min", "OpenCV Window", 0, 179, pass_) #~179
cv2.createTrackbar("H_max", "OpenCV Window", 128, 179, pass_)
cv2.createTrackbar("S_min", "OpenCV Window", 128, 255, pass_)
cv2.createTrackbar("S_max", "OpenCV Window", 255, 255, pass_)
cv2.createTrackbar("V_min", "OpenCV Window", 128, 255, pass_)
cv2.createTrackbar("V_max", "OpenCV Window", 255, 255, pass_)

points_list = []
color_list = []
for i in range(10):
  color_list.append((random.randint(0,255), random.randint(0,255), random.randint(0,255)))
  points_list.append([random.randint(0,x_img),random.randint(0,y_img),1])

points = np.float32(points_list)


try:
  while True:

    h_min = cv2.getTrackbarPos("H_min", "OpenCV Window")
    h_max = cv2.getTrackbarPos("H_max", "OpenCV Window")
    s_min = cv2.getTrackbarPos("S_min", "OpenCV Window")
    s_max = cv2.getTrackbarPos("S_max", "OpenCV Window")
    v_min = cv2.getTrackbarPos("V_min", "OpenCV Window")
    v_max = cv2.getTrackbarPos("V_max", "OpenCV Window")

    mask_img = cv2.inRange(hsv_img, (h_min, s_min, v_min), (h_max, s_max, v_max))
    masked_img = cv2.bitwise_and(hsv_img, hsv_img, mask=mask_img)
    masked_img = cv2.cvtColor(masked_img, cv2.COLOR_HSV2RGB)
    masked_img = cv2.GaussianBlur(masked_img,(3,3),1)

    num_labels, label, stats, centers = cv2.connectedComponentsWithStats(mask_img)
    num_labels = num_labels - 1
    stats = np.delete(stats, 0, 0)
    centers = np.delete(centers, 0, 0)
    result_img = img.copy()
    marked_img = masked_img.copy()
    if num_labels >= 4:
        order = np.argsort(stats[:,4])[::-1]
        stats = stats[order][:4, :]
        centers = centers[order][:4, :]

        for stat in stats:
          result_img = cv2.rectangle(result_img, (stat[0],stat[1]), (stat[0]+stat[2],stat[1]+stat[3]), (255,50,50),2)
        
        image_centor_x = 0
        image_centor_y = 0
        for center in centers:
          image_centor_x += center[0]
          image_centor_y += center[1]
        image_centor_x = image_centor_x/4
        image_centor_y = image_centor_y/4
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
        src_corner = np.float32([corners["UL"], corners["UR"], corners["LL"], corners["LR"]])
        dst_corner = np.float32([[0,0],[x_img,0],[0,y_img],[x_img,y_img]])
        matrix = cv2.getPerspectiveTransform(src_corner,dst_corner)
       
        result_img = cv2.warpPerspective(result_img, matrix, (x_img, y_img))
        print(result_img.shape)
        array = np.float32([0,0])
        for arr in src_corner:
          arr = np.append(arr, 1)
          print(np.matmul(matrix, arr))
        print("   ")
        print("   ")
        print("   ")


        #for i in range(len(points)):
        #  marked_img = cv2.circle(marked_img,(int(points[i][0]),int(points[i][1])), 10, color_list[i], thickness=3)
          #cv2.perspectiveTransform(points[i], array, matrix)
        #  array = np.matmul(matrix, points[i])
        #  result_img = cv2.circle(result_img, (int(array[0]),int(array[1])), 10, color_list[i], thickness=3)

    cv2.imshow("masked image", marked_img)
    cv2.imshow("result image",result_img)
    key = cv2.waitKey(1)
    if key == 27:
      break

except(KeyboardInterrupt,SystemExit):
  print("exit")
