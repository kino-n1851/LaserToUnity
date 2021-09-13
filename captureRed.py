import cv2
import numpy as np
"""
for i in range(50):
  cap = cv2.VideoCapture(i-1)
  if cap.isOpened():
    print(i-1)
"""

img = cv2.imread('aaa.png')
x_img,y_img = img.shape[0], img.shape[1]
list_x = []
list_y = []
x=0
y=0

print(str(x_img)+":"+str(y_img))

for i in range(x_img):
  for j in range(y_img):
    if img[i][j][0] < 250:
      x = x + i
      y = y + j
      list_x.append(i)
      list_y.append(j)

print(list_x)
print(list_y)
x_avg = x / (len(list_x) * x_img)
y_avg = y / (len(list_y) * y_img)
print(str(x_avg)+":"+str(y_avg))
cv2.imshow("a",img)
cv2.waitkey(0)
