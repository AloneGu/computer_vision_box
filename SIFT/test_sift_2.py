import cv2
import numpy as np
import matplotlib.pyplot as plt
#import pdb
#pdb.set_trace()#turn on the pdb prompt

fig = plt.figure()
a = fig.add_subplot(1,2,1)

#read image
img = cv2.imread('../data/box.png',cv2.IMREAD_COLOR)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
plt.imshow(img)
a.set_title('org')


#SIFT
detector = cv2.SIFT()
keypoints = detector.detect(gray,None)
img = cv2.drawKeypoints(gray,keypoints)
#img = cv2.drawKeypoints(gray,keypoints,flags = cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
a=fig.add_subplot(1,2,2)
plt.imshow(img)
a.set_title('test')

plt.show()