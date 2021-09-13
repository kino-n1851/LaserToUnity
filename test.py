import cv2
from datetime import datetime

cap = cv2.VideoCapture(0) # 任意のカメラ番号に変更する

while True:
    ret, frame = cap.read()
    cv2.imshow("camera", frame)

    k = cv2.waitKey(1)&0xff # キー入力を待つ
    if k == ord('p'):
        # 「p」キーで画像を保存
        date = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = "./img/" + date + ".png"
        cv2.imwrite(path, frame) # ファイル保存

        cv2.imshow(path, frame) # キャプチャした画像を表示
    elif k == ord('q'):
        # 「q」キーが押されたら終了する
        break

# キャプチャをリリースして、ウィンドウをすべて閉じる
cap.release()
cv2.destroyAllWindows()