from pathlib import Path

import numpy as np
from django_pandas.io import pd
import cv2
from cv2 import aruco


CURRENT_DIR = Path(__file__).resolve().parent


def bgr2hsv(bgr, lower, upper):
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    return cv2.inRange(hsv, lower, upper)


def gen_pai_df(arr):
    river = list(map(lambda pai: f'./static/image/pai/{pai}.jpg', arr))
    for _ in range(6 - len(river) % 6):
        river.append(None)
    river = np.array(river).reshape(-1, 6)
    df = pd.DataFrame(
        river,
    )
    return df


class Analyze:

    def __init__(self, img):
        self.trg_img = img

    def detect(self):
        p_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
        corners, ids, _ = aruco.detectMarkers(self.trg_img, p_dict)
        return corners, ids

    def trans(self, points):
        p_1, p_2, p_3, p_4 = points

        x, y = (p_4[0] - p_1[0] - 10, - p_4[1] + p_1[1])
        width, height = (500, 500)

        marker_coordinates = np.float32([p_1, p_2, p_3, p_4])
        true_coordinates   = np.float32([[x, y], [x + width, y], [x + width, y + height], [x, y + height]])
        trans_mat = cv2.getPerspectiveTransform(marker_coordinates, true_coordinates)
        img_trans = cv2.warpPerspective(self.trg_img, trans_mat, (int(width * 1.05), height))
        return img_trans

    def findcnt(self, img_trans, hsv_mask):
        cnts, _ = cv2.findContours(hsv_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnt = max(cnts, key=cv2.contourArea)
        epsilon = 70
        approx = cv2.approxPolyDP(cnt, epsilon, True)
        src_aff = np.float32([approx[0, 0], approx[1, 0], approx[-1, 0]])
        w, h = np.linalg.norm(approx[0] - approx[-1]), np.linalg.norm(approx[0] - approx[1])
        dst_aff = np.float32([[0, 0], [0, h], [w, 0]])
        mat = cv2.getAffineTransform(src_aff, dst_aff)
        affine_img = cv2.warpAffine(img_trans, mat, (int(w), int(h)))
        return affine_img

    def read_river(self, person):
        corners, ids = self.detect()
        p_1 = corners[np.where(ids == 0)[0][0]][0, 2]
        p_2 = corners[np.where(ids == 3)[0][0]][0, 3]
        p_3 = corners[np.where(ids == 2)[0][0]][0, 0]
        p_4 = corners[np.where(ids == 1)[0][0]][0, 1]
        img_trans = self.trans([p_1, p_2, p_3, p_4])
        hsv_mask = bgr2hsv(img_trans, np.array([0, 0, 200]), np.array([255, 255, 255]))
        affine_img = self.findcnt(img_trans, hsv_mask)
        affine_hsv_mask = bgr2hsv(affine_img, np.array([0, 0, 150]), np.array([255, 255, 255]))
        river_chunk = []
        for row_img in np.array_split(affine_hsv_mask, 3, axis=0):
            for pai in np.array_split(row_img, 6, axis=1):
                river_chunk.append(pai)
        river_chunk = river_chunk[:-1]
        base_path = str(CURRENT_DIR / 'data/base.jpg')
        base_img = cv2.imread(base_path)
        base_img = cv2.resize(base_img, (82 * 9, 115 * 4))
        base_hsv_mask = bgr2hsv(base_img, np.array([0, 0, 150]), np.array([255, 255, 255]))
        base_chunk = []
        for row_img in np.array_split(base_hsv_mask, 4, axis=0):
            for chunk in np.array_split(row_img, 9, axis=1):
                base_chunk.append(chunk)
        base_chunk = base_chunk[:-2]

        bf = cv2.BFMatcher(cv2.NORM_HAMMING)
        detector = cv2.AKAZE_create()
        pai_arr = [
            '1m', '2m', '3m', '4m', '5m', '6m', '7m', '8m', '9m',
            '1p', '2p', '3p', '4p', '5p', '6p', '7p', '8p', '9p',
            '1s', '2s', '3s', '4s', '5s', '6s', '7s', '8s', '9s',
            '1z', '2z', '3z', '4z', '5z', '6z', '7z'
            
        ]

        res_arr = []
        for pai in river_chunk:
            _, target_des = detector.detectAndCompute(pai, None)
            res_i = -1
            res = 100000
            for i, bi in enumerate(base_chunk):
                try:
                    _, comparing_des = detector.detectAndCompute(bi, None)
                    matches = bf.match(target_des, comparing_des)
                    dist = [m.distance for m in matches]
                    ret = sum(dist) / len(dist)
                except cv2.error:
                    ret = 100000
                if res > ret:
                    res = ret
                    res_i = i
            res_arr.append(pai_arr[res_i])
        return res_arr
