import numpy as np
import cv2


def process_imgs_box(img1, img2, one_box):
    img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    x, y, w, h = one_box
    x = max(0, x - w / 2)
    y = max(0, y - h / 2)
    y = min(320, y)
    x = min(480, x)
    box_content = img1[y:y + h, x:x + w, :]
    sift = cv2.SIFT()
    kp1, des1 = sift.detectAndCompute(box_content, None)
    kps = []
    for k in kp1:
        kps.append([[k.pt[0], k.pt[1]], k.response])
    kps = sorted(kps, key=lambda x: x[1], reverse=True)
    kps = kps[:20]
    x_sum = 0
    y_sum = 0
    for k in kps:
        k[0][0] += x
        k[0][1] += y
        x_sum += k[0][0]
        y_sum += k[0][1]
    org_pos = np.array([x_sum / 20, y_sum / 20])

    for k in kps:
        x1, y1 = k[0]
        cv2.circle(img1, (int(x1), int(y1)), 4, (255, 0, 0), 1)

    p0 = np.float32([k[0] for k in kps])
    res = cv2.calcOpticalFlowPyrLK(img1_gray, img2_gray, p0)
    final_pos = np.mean(res[0], axis=0)

    for k in kps:
        x1, y1 = k[0]
        cv2.circle(img2, (int(x1), int(y1)), 4, (0, 255, 0), 1)
    return org_pos, final_pos


img1 = cv2.imread('../data/orgimg_102.jpg')  # queryImage
img2 = cv2.imread('../data/orgimg_103.jpg')  # trainImage
box = [129, 68, 48, 89]
print process_imgs_box(img1, img2, box)
cv2.imshow('t',img1)
cv2.imshow('t2',img2)
cv2.waitKey(0)
cv2.destroyAllWindows()
