import numpy as np
import cv2
import os
from sklearn.svm import SVC

WINSIZE = (64, 64)
BLOCKSIZE = (16, 16)
BLOCKSTRIDE = (8, 8)
CELLSIZE = (8, 8)
NBINS = 9


class HogSvmProcessor:
    def __init__(self, img_dir, pos_dict, neg_dict):
        self.img_dir = img_dir
        self.old_pos_dict = pos_dict
        self.old_neg_dict = neg_dict
        self.features = []
        self.response = []
        self.hog_worker = cv2.HOGDescriptor(WINSIZE, BLOCKSIZE, BLOCKSTRIDE, CELLSIZE, NBINS)
        self.svm_cls = SVC()

    def run(self):
        self.get_features()
        self.svm_train()
        self.get_cls_score()

    def get_features(self):
        # prepare pos data
        for k in self.old_pos_dict:
            tmp_f_path = os.path.join(self.img_dir, k)
            for b in self.old_pos_dict[k]:
                x, y, w, h = b
                frame = cv2.imread(tmp_f_path, 0)
                tmp_frame = frame[y:y + h, x:x + w]
                tmp_frame = cv2.resize(tmp_frame, WINSIZE)
                tmp_hog_feature = self.hog_worker.compute(tmp_frame)
                self.features.append(tmp_hog_feature)
                self.response.append(1)
        print 'get pos data', len(self.features)
        # prepare neg data
        for k in self.old_neg_dict:
            tmp_f_path = os.path.join(self.img_dir, k)
            for b in self.old_neg_dict[k]:
                x, y, w, h = b
                frame = cv2.imread(tmp_f_path, 0)
                tmp_frame = frame[y:y + h, x:x + w]
                tmp_hog_feature = self.hog_worker.compute(tmp_frame)
                self.features.append(tmp_hog_feature)
                self.response.append(0)
        data_len = len(self.features)
        hog_feature_len = len(self.features[0])
        print 'get neg data', len(self.features)
        self.features = np.array(self.features)
        # fix this error: ValueError: Found array with dim 3. Estimator expected <= 2.
        self.features = np.reshape(self.features, (data_len, hog_feature_len))
        self.response = np.array(self.response)

    def svm_train(self):

        self.svm_cls.fit(self.features, self.response)

    def get_cls_score(self):
        print self.svm_cls.score(self.features, self.response)


if __name__ == '__main__':
    pos = eval(open('/home/jac/Documents/work_tmp/8100224_2016-03-05/old_pos.txt').read())
    neg = eval(open('/home/jac/Documents/work_tmp/8100224_2016-03-05/old_neg.txt').read())
    img_dir = '/home/jac/Documents/work_tmp/8100224_2016-03-05/imgs'
    t = HogSvmProcessor(img_dir, pos, neg)
    t.run()
