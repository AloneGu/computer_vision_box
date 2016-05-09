import cv2
img = cv2.imread('../data/orgimg_102.jpg')
cv2.line(img,(280,210),(380,210),(0,0,0))
cv2.imshow('t',img)
cv2.waitKey(0)
cv2.destroyAllWindows()