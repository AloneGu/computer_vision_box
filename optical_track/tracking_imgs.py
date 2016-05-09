import os
import numpy as np
import cv2

IMGS = '../download_box_data/org_imgs'
BOX_FILE = '../download_box_data/bbox.txt'
LOI_LEFT = (280, 210)
LOI_RIGHT = (380, 210)
KPOINTS = 20
JUMP_MIN = 3
JUMP_MAX = 8
DIS_PARAMETER = 300


def ccw(A, B, C):
    x1 = A[0] - B[0]
    x2 = A[0] - C[0]
    y1 = A[1] - B[1]
    y2 = A[1] - C[1]
    return 1 if x1 * y2 > x2 * y1 else -1


# Return true if line segments AB and CD intersect
def intersect(A, B, C, D):
    if A == C or A == D or B == C or B == D:
        return True
    res_a = ccw(A, B, C) * ccw(A, B, D)
    res_b = ccw(B, A, C) * ccw(B, A, D)
    if res_a < 0 and res_b < 0:
        return True
    else:
        return False


def cal_d(A, B):
    return (A[0] - B[0]) ** 2 + (A[1] - B[1]) ** 2


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
    kps = kps[:KPOINTS]
    x_sum = 0
    y_sum = 0
    for k in kps:
        k[0][0] += x
        k[0][1] += y
        x_sum += k[0][0]
        y_sum += k[0][1]
    org_pos = np.array([x_sum / KPOINTS, y_sum / KPOINTS])

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


class ImageTracker(object):
    def __init__(self):
        tmp_list = os.listdir(IMGS)
        self.imgs_path = []
        for f in tmp_list:
            self.imgs_path.append(os.path.join(IMGS, f))
        self.imgs_path = sorted(self.imgs_path, key=lambda x: filter(lambda y: y.isdigit(), x))

        tmp_content = eval(open(BOX_FILE).read())
        self.box_dict = {}
        for tmp_d in tmp_content:
            self.box_dict[tmp_d['name']] = tmp_d['bbox_res']
        self.walkin, self.walkout = 0, 0

    def run(self):
        self.res = []
        imgs_count = len(self.imgs_path)
        for i in range(imgs_count - 1):
            img1 = cv2.imread(self.imgs_path[i])
            img2 = cv2.imread(self.imgs_path[i + 1])
            file_key = os.path.basename(self.imgs_path[i])
            for b in self.box_dict[file_key]:
                try:
                    x, y, _, _ = b
                    if x < 240 or x > 450 or y < 160 or y > 300:  # ROI
                        continue
                    old, new = process_imgs_box(img1, img2, b)
                    self.res.append([old, new, self.imgs_path[i]])
                except:
                    print self.imgs_path[i], b
        res_len = len(self.res)
        print res_len
        i = 0
        while i < res_len:
            old, new, f = self.res[i]
            old = [int(old[0]), int(old[1])]
            new = [int(new[0]), int(new[1])]
            if intersect(old, new, LOI_LEFT, LOI_RIGHT):
                dis = cal_d(old, new)
                jump_idx = int(max(JUMP_MIN, DIS_PARAMETER / dis))
                jump_idx = min(JUMP_MAX, jump_idx)
                if old[1] < LOI_LEFT[1]:
                    self.walkin += 1
                    print f, 'walkin', dis, jump_idx
                else:
                    self.walkout += 1
                    print f, 'walkout', dis, jump_idx
                i += jump_idx
            else:
                i += 1
        print self.walkin, self.walkout


if __name__ == '__main__':
    t = ImageTracker()
    t.run()
    # print intersect([0, 0], [1, 1], [1, 0], [0, 1])
    #
    # print intersect([0, 0], [1, 1], [1, 0], [0, 0])
    # print intersect([0, 0], [1, 1], [1, 0], [3, 0])
