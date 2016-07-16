import cv2
cap1 = cv2.VideoCapture('./l.mp4')
cap2 = cv2.VideoCapture('./r.mp4')
imgs1 = []
imgs2 = []
while True:
    ret, tmp_img = cap1.read()
    imgs1.append(tmp_img)
    if not ret:
        break
cap1.release()
while True:
    ret, tmp_img = cap2.read()
    imgs2.append(tmp_img)
    if not ret:
        break
cap2.release()

v_len = min(len(imgs1), len(imgs2))
print len(imgs1), len(imgs2),type(imgs1[0]), imgs1[0].shape
w, h, _ = imgs1[0].shape
fps = 24
fcc = cv2.cv.CV_FOURCC('F','L','V','1')
videoWriter = cv2.VideoWriter('./res.flv', fcc, fps, (w, h))
for i in range(v_len):
    try:
        tmp_img = imgs1[i]
        tmp_img[:, h / 2:, :] = imgs2[i][:, h / 2:, :]
        cv2.imshow('t', tmp_img)
        cv2.waitKey(1000 / 24)
        videoWriter.write(tmp_img)
    except:
        pass
cv2.destroyAllWindows()

