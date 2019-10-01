from PIL import Image
import cv2
import math
from scipy.linalg import solve
import numpy as np
from copy import copy
from matplotlib import pyplot as plt

class ReceiptImageService():
    def __init__(self, imagepath):
        self.org = cv2.imread(imagepath)
        self.org = cv2.resize(self.org, None, fx=0.5, fy=0.5)
        self.img = copy(self.org)

        self.text = ""
        self.gray = cv2.cvtColor(self.img, cv2.COLOR_RGB2GRAY)
        self.lines = []
        self.corners = []

    def transform(self,corners):
        x = max(corners[1][0] - corners[0][0], corners[2][0] - corners[3][0])
        y = max(corners[3][1] - corners[0][1], corners[3][1] - corners[2][1])
        dst = np.float32([(0,0),(x,0),(x,y),(0,y)])
        corners = np.float32(corners)
        m = cv2.getPerspectiveTransform(corners,dst)
        self.trsfmd = cv2.warpPerspective(self.org,m,(x,y))


    def findCorners(self):
        bi = cv2.adaptiveThreshold(self.gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,5)
        edges = cv2.Canny(bi, 130, 130, apertureSize=3)
        borders = self.findBorders(edges)
        #cv2.imshow("xx", bi)
        nw = [[borders[0][0], borders[0][1]], [borders[2][0], borders[2][1]]]
        ww_nw = [-borders[0][2], -borders[2][2]]
        sw = [[borders[0][0], borders[0][1]], [borders[3][0], borders[3][1]]]
        ww_sw = [-borders[0][2], -borders[3][2]]
        ne = [[borders[1][0], borders[1][1]], [borders[2][0], borders[2][1]]]
        ww_ne = [-borders[1][2], -borders[2][2]]
        se = [[borders[1][0], borders[1][1]], [borders[3][0], borders[3][1]]]
        ww_se = [-borders[1][2], -borders[3][2]]
        m = (nw,ne,se,sw)
        ww = (ww_nw,ww_ne,ww_se,ww_sw)
        corners = []
        for i in range(len(m)):
            temp = solve(m[i],ww[i])
            point_temp = tuple([int(i) for i in temp])
            corners.append(point_temp)
            self.img = cv2.circle(self.img, point_temp, 5, (0, 255, 0), thickness=2)
           #cv2.imshow('edges', self.img)
            #cv2.waitKey()
        self.corners = corners
        return corners

    def tc(self,r1,t1,r2,t2,epsA,epsB):
        if abs(r1-r2)<epsA and abs(t1-t2)<epsB:
            return True
        else:
            return False

    def findBorders(self, edges):
        lines = cv2.HoughLines(edges, 1, math.pi / 180, 50)
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
                cv2.imshow("xd",self.img)
                cv2.waitKey()
                ind += 1
        self.lines = result
        return result

    @staticmethod
    def distance(pnt, line):
        x, y = pnt
        A, B, C = line
        return abs(A * x + B * y + C) / math.sqrt(A ** 2 + B ** 2)

    def distanseTuple(self, lines):
        result = []
        ind = 0
        for line in lines:
            for rho, theta in line:
                A = math.cos(theta)
                B = math.sin(theta)
                C = -rho
                #  0 - dlugosc  1 - szerokosc
                left_center = (0, self.img.shape[0] // 2)
                right_center = (self.img.shape[1], self.img.shape[0] // 2)
                top_center = (self.img.shape[1] // 2, 0)
                bottom_center = (self.img.shape[1] // 2, self.img.shape[0])
                line_p = (A, B, C)
                try:
                    distance_left = self.distance(left_center,
                                                  line_p)*(ind+1) if theta < math.pi / 12 or theta > 11 * math.pi / 12 else 10000
                    distance_right = self.distance(right_center,
                                                   line_p)*(ind+1) if theta < math.pi / 12 or theta > 11 * math.pi / 12 else 10000
                except (ZeroDivisionError, ArithmeticError):
                    distance_left = self.distance(left_center, line_p)*(ind+1)
                    distance_right = self.distance(right_center, line_p)*(ind+1)
                try:
                    distance_top = self.distance(top_center,
                                                 line_p)*(ind+1) if 5 * math.pi / 12 < theta < 7 * math.pi / 12 else 10000
                    distance_bottom = self.distance(bottom_center,
                                                    line_p)*(ind+1) if 5 * math.pi / 12 < theta < 7 * math.pi / 12 else 10000
                except (ZeroDivisionError, ArithmeticError):
                    distance_top = 10000
                    distance_bottom = 10000
                el = (distance_left, distance_right, distance_top, distance_bottom, ind)
                result.append(el)
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

    def dv(self):
        result = []
        ind = 0
        ho = 0
        vert = 0
        for line in lines:
            for rho, theta in line:
                ap = False
                if 5 * math.pi / 12 < theta < 7 * math.pi / 12 and ho < 2:
                    ho += 1
                    ap = True
                    print("ho ", ho)
                if (theta < math.pi / 12 or theta > 11 * math.pi / 12) and vert < 2:
                    vert += 1
                    ap = True
                    print("vert", vert)
                if (ap):
                    result.append(ind)
                ind += 1
        return result


ris = ReceiptImageService('img5.jpg')

x= ris.findCorners()
ris.transform(x)
cv2.imshow("org",ris.img)
#cv2.imshow("tr",ris.trsfmd)
plt.hist(ris.trsfmd.ravel(),256,[0,256])
bi = cv2.adaptiveThreshold(cv2.cvtColor(ris.trsfmd, cv2.COLOR_RGB2GRAY),255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,5)
cv2.imshow("tr",bi)
plt.show()
cv2.waitKey()