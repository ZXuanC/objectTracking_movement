import cv2
import numpy as np

cap = cv2.VideoCapture(0)

width = 1280
height = 960

cap = cv2.VideoCapture(0)

# 設定影像尺寸
width = 1280
height = 960

# 設定擷取影像的尺寸大小
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)


# 初始化平均影像
ret, frame = cap.read()
avg = cv2.blur(frame, (4, 4))
avg_float = np.float32(avg)

while True:

  ret, frame = cap.read()

  diff = cv2.absdiff(avg, frame)


  gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)


  ret, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)

  thresh = cv2.erode(thresh, None, iterations=2)
  thresh = cv2.dilate(thresh, None, iterations=2)

  cntImg, cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

  for i in cnts:
    # 忽略太小的區域
    if cv2.contourArea(i) < 2500:
      continue

    # 計算等高線的外框範圍
    (x, y, w, h) = cv2.boundingRect(i)

    # 畫出外框
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)


  # 顯示偵測結果影像
  cv2.imshow('frame', frame)

  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

  # 更新平均影像
  cv2.accumulateWeighted(frame, avg_float,0.1)
  avg = cv2.convertScaleAbs(avg_float)

cap.release()
cv2.destroyAllWindows()