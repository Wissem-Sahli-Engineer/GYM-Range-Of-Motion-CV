import math
from math import cos
import time, math
import cv2


# init " pTime = time.time() " before the While loop
def get_fps(cap, pTime,type='default'):
    if type == "default":
        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime
        return fps, pTime

    elif type =="cap":
        fps= cap.get(cv2.CAP_PROP_FPS)
        if fps<= 0:
            return 30, pTime
        return fps, pTime
    else:
        return 30, pTime


def get_dist(point1,point2):
    return math.hypot(point1[1]-point2[1],point1[2]-point2[2])

# a and b form the angle
def get_angle(a,b,c):
    return math.degrees(math.acos((a**2 + b**2 - c**2) / ( 2 * a * b) ))
