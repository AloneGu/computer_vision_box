import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread('../data/img_103.jpg')
x, y, w, h = [129, 68, 48, 89]
x = max(0, x - w / 2)
y = max(0, y - h / 2)
y = min(320, y)
x = min(480, x)
box_content = img[y:y + h, x:x + w, :]
gray = cv2.cvtColor(box_content,cv2.COLOR_BGR2GRAY)

corners = cv2.goodFeaturesToTrack(gray,10,0.01,10)
print corners
corners = np.int0(corners)

for i in corners:
    x1,y1 = i.ravel()
    cv2.circle(img,(x+x1,y+y1),3,255,-1)

plt.imshow(img),plt.show()