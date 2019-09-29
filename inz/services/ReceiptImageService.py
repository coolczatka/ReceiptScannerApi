from PIL import Image
import cv2
import math
import numpy as np
from scipy.linalg import solve


class ReceiptImageService():
    def __init__(self, imagepath):
        self.img = cv2.imread(imagepath)
        self.img = cv2.resize(self.img, None, fx=0.5, fy=0.5)
        self.text = ""
        self.gray = cv2.cvtColor(self.img, cv2.COLOR_RGB2GRAY)

    def findCorners(self):
        edges = cv2.Canny(self.gray, 130, 130, apertureSize=3)
        borders = self.findBorders(edges)
        nw = [[borders[0][0], borders[0][1]], [borders[2][0], borders[2][1]]]
        sw = [[borders[0][0], borders[0][1]], [borders[3][0], borders[3][1]]]

    def findBorders(self, edges):
        lines = cv2.HoughLines(edges, 1, np.pi / 180, 70)
        indexes = self.indexes(lines)
        list_of_index = []
        for i in indexes:
            _, index = i[0]
            list_of_index.append(index)
        result = []
        ind = 0

        for line in list_of_index:
            for rho, theta in lines[line]:
                A = math.cos(theta)
                B = math.sin(theta)
                C = -rho
                result.append([A, B, C])

                x0 = A * rho
                y0 = B * rho
                x1 = int(x0 + 1000 * -B)
                y1 = int(y0 + 1000 * A)
                x2 = int(x0 - 1000 * -B)
                y2 = int(y0 - 1000 * A)
                self.img = cv2.line(self.img, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.imshow('edges', self.img)
                ind += 1
                cv2.waitKey()
        return result

    @staticmethod
    def distance(pnt, line):
        x, y = pnt
        A, B, C = line
        return abs(A * x + B * y + C) / np.sqrt(A ** 2 + B ** 2)

    def distanseTuple(self, lines):
        result = []
        ind = 0
        for line in lines:
            for rho, theta in line:
                A = math.cos(theta)
                B = math.sin(theta)
                C = -rho
                print(theta)
                left_center = (0, self.img.shape[0] // 2)
                right_center = (self.img.shape[1], self.img.shape[0] // 2)
                top_center = (self.img.shape[1] // 2, 0)
                bottom_center = (self.img.shape[1] // 2, self.img.shape[0])
                line_p = (A, B, C)
                try:
                    distance_left = self.distance(left_center,
                                                  line_p) if theta < math.pi / 12 or theta > 11 * math.pi / 12 else 10000
                    distance_right = self.distance(right_center,
                                                   line_p) if theta < math.pi / 12 or theta > 11 * math.pi / 12 else 10000
                except (ZeroDivisionError, ArithmeticError):
                    distance_left = self.distance(left_center, line_p)
                    distance_right = self.distance(right_center, line_p)
                try:
                    distance_top = self.distance(top_center,
                                                 line_p) if 5 * math.pi / 12 < theta < 7 * math.pi / 12 else 10000
                    distance_bottom = self.distance(bottom_center,
                                                    line_p) if 5 * math.pi / 12 < theta < 7 * math.pi / 12 else 10000
                except (ZeroDivisionError, ArithmeticError):
                    distance_top = 10000
                    distance_bottom = 10000
                result.append((distance_left, distance_right, distance_top, distance_bottom, ind))
                ind += 1
        return result

    def indexes(self, lines):
        dt = self.distanseTuple(lines)
        q = []
        for i in range(4):
            dt.sort(key=lambda x: x[i])
            ind = [(j[i], j[4]) for j in dt]
            q.append(ind)
        return q


ris = ReceiptImageService('img4.jpg')
ris.findCorners()
