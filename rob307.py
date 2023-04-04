'''import cv2
import os

#RTSP_URL = 'rtsp://admin:rtsoft123@10.5.20.199:554/cam/realmonitor?channel=3&subtype=0'

os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS'] = 'rtsp_transport;udp'

#cap = cv2.VideoCapture(RTSP_URL, cv2.CAP_FFMPEG)
cap= cv2.VideoCapture(0)
if not cap.isOpened():
    print('Cannot open RTSP stream')
    exit(-1)

while True:
    _, frame = cap.read()
    cv2.imshow('RTSP stream', frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()'''
from __future__ import print_function
import cv2 as cv
import argparse
import sys
import numpy as np

import math

max_value = 255
max_value_H = 360//2
low_H = 0
low_S = 0
low_V = 0
high_H = max_value_H
high_S = max_value
high_V = max_value
window_capture_name = 'Video Capture'
window_detection_name = 'Object Detection'
low_H_name = 'Low H'
low_S_name = 'Low S'
low_V_name = 'Low V'
high_H_name = 'High H'
high_S_name = 'High S'
high_V_name = 'High V'
def on_low_H_thresh_trackbar(val):
    global low_H
    global high_H
    low_H = val
    low_H = min(high_H-1, low_H)
    cv.setTrackbarPos(low_H_name, window_detection_name, low_H)
def on_high_H_thresh_trackbar(val):
    global low_H
    global high_H
    high_H = val
    high_H = max(high_H, low_H+1)
    cv.setTrackbarPos(high_H_name, window_detection_name, high_H)
def on_low_S_thresh_trackbar(val):
    global low_S
    global high_S
    low_S = val
    low_S = min(high_S-1, low_S)
    cv.setTrackbarPos(low_S_name, window_detection_name, low_S)
def on_high_S_thresh_trackbar(val):
    global low_S
    global high_S
    high_S = val
    high_S = max(high_S, low_S+1)
    cv.setTrackbarPos(high_S_name, window_detection_name, high_S)
def on_low_V_thresh_trackbar(val):
    global low_V
    global high_V
    low_V = val
    low_V = min(high_V-1, low_V)
    cv.setTrackbarPos(low_V_name, window_detection_name, low_V)
def on_high_V_thresh_trackbar(val):
    global low_V
    global high_V
    high_V = val
    high_V = max(high_V, low_V+1)
    cv.setTrackbarPos(high_V_name, window_detection_name, high_V)
def rects(framme, color):
    contours0, hierarchy = cv.findContours( framme.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)  
        # перебираем все найденные контуры в цикле
    for cnt in contours0:
        rect = cv.minAreaRect(cnt) # пытаемся вписать прямоугольник
        box = cv.boxPoints(rect) # поиск четырех вершин прямоугольника
        box = np.int0(box) # округление координат
        a=((box[0][0] - box[1][0])**2+(box[0][1] - box[1][1])**2)**0.5
        b=((box[0][0] - box[3][0])**2+(box[0][1] - box[3][1])**2)**0.5
        s=int(a*b)
        if s>500:
            #xy=[box[0][0],box[0][1]]
            cv.drawContours(frame,[box],0,(color[0],color[1],color[2]),2)
            #if box[0][1] - box[1][1]<0:
                #xy[0]=
            #print(color[3]+)
parser = argparse.ArgumentParser(description='Code for Thresholding Operations using inRange tutorial.')
parser.add_argument('--camera', help='Camera divide number.', default=0, type=int)
args = parser.parse_args()
cap = cv.VideoCapture(args.camera)
#cv.namedWindow(window_capture_name)
cv.namedWindow(window_detection_name+'1')
cv.namedWindow(window_detection_name+'2')
'''cv.createTrackbar(low_H_name, window_detection_name , low_H, max_value_H, on_low_H_thresh_trackbar)
cv.createTrackbar(high_H_name, window_detection_name , high_H, max_value_H, on_high_H_thresh_trackbar)
cv.createTrackbar(low_S_name, window_detection_name , low_S, max_value, on_low_S_thresh_trackbar)
cv.createTrackbar(high_S_name, window_detection_name , high_S, max_value, on_high_S_thresh_trackbar)
cv.createTrackbar(low_V_name, window_detection_name , low_V, max_value, on_low_V_thresh_trackbar)
cv.createTrackbar(high_V_name, window_detection_name , high_V, max_value, on_high_V_thresh_trackbar)'''
while True:
    
    ret, frame = cap.read()
    if frame is None:
        break
    frame_HSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    frame_threshold1 = cv.inRange(frame_HSV, (150, 119, 187), (186, 255, 255))
    frame_threshold2 = cv.inRange(frame_HSV, (85, 200, 120), (130, 255, 255))
    
    
    #cv.imshow(window_capture_name, frame)
 
    rects(frame_threshold1, [0,0,255,'red'])
    rects(frame_threshold2, [255,0,0,'blue'])
    cv.imshow('contur', frame)        
    cv.imshow(window_detection_name+'1', frame_threshold1)
    cv.imshow(window_detection_name+'2', frame_threshold2)
       
    
    key = cv.waitKey(30)
    if key == ord('q') or key == 27:
        break