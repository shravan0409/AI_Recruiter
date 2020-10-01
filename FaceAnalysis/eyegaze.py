# -*- coding: utf-8 -*-
"""
Created on Tue Dec 24 18:20:15 2019

@author: Vaishali
"""
import cv2
import dlib
from math import hypot 
import numpy as np
import time

cap=cv2.VideoCapture(0)
detector=dlib.get_frontal_face_detector()
predictor=dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
fourcc=cv2.VideoWriter_fourcc(*'XVID')
out=cv2.VideoWriter('output.avi',fourcc,7,(640,480))

def eye_gaze(landmark):
    lleft_point=(landmark.part(36).x,landmark.part(36).y)
    lright_point=(landmark.part(39).x,landmark.part(39).y)
    #lhorline=cv2.line(frame,lleft_point,lright_point,(0,255,0),1)
    lcenter_top=midpoint(landmark.part(37),landmark.part(38))
    lcenter_bottom=midpoint(landmark.part(41),landmark.part(40))
    #lver_line=cv2.line(frame,lcenter_top,lcenter_bottom,(0,255,0),1)
    
    rleft_point=(landmark.part(42).x,landmark.part(42).y)
    rright_point=(landmark.part(45).x,landmark.part(45).y)
    #rhorline=cv2.line(frame,rleft_point,rright_point,(0,255,0),1)
    rcenter_top=midpoint(landmark.part(43),landmark.part(44))
    rcenter_bottom=midpoint(landmark.part(47),landmark.part(46))
    #rver_line=cv2.line(frame,rcenter_top,rcenter_bottom,(0,255,0),1)
    
    lhorline_length=hypot((lleft_point[0]-lright_point[0]),(lleft_point[1]-lright_point[1]))
    lver_line_length=hypot((lcenter_top[0]-lcenter_bottom[0]),(lcenter_top[1]-lcenter_bottom[1]))
    left_ratio=(lhorline_length/lver_line_length)
    rhorline_length=hypot((rleft_point[0]-rright_point[0]),(rleft_point[1]-rright_point[1]))
    rver_line_length=hypot((rcenter_top[0]-rcenter_bottom[0]),(rcenter_top[1]-rcenter_bottom[1]))
    right_ratio=(rhorline_length/rver_line_length)
    ratio=(left_ratio+right_ratio)/2
    
    #lefteye=np.array([(landmark.part(36).x,landmark.part(36).y),(landmark.part(37).x,landmark.part(37).y),(landmark.part(38).x,landmark.part(38).y),(landmark.part(39).x,landmark.part(39).y),(landmark.part(40).x,landmark.part(40).y),(landmark.part(41).x,landmark.part(41).y)],np.int32)
    #cv2.polylines(frame,[lefteye],True,(255,0,255),2)
    #eyeregion=frame[]
    
    if ratio > 5.23:
        print("eyes not on screen ")
    return

def face_movement(landmark):
    fx=landmark.part(1).x
    fy=landmark.part(1).y
    cv2.circle(frame,(fx,fy),3,(255,0,0),2)
    fx1=landmark.part(15).x
    fy1=landmark.part(15).y
    cv2.circle(frame,(fx1,fy1),3,(255,0,0),2)
    nx=landmark.part(29).x
    ny=landmark.part(29).y
    cv2.circle(frame,(nx,ny),3,(255,0,0),2)
    cx=landmark.part(8).x
    cy=landmark.part(8).y
    cv2.circle(frame,(cx,cy),3,(255,0,0),2)
    rface_length=hypot((fx-nx),(fy-ny))
    lface_length=hypot((nx-fx1),(ny-fy1))
    #ratio=(rface_length+lface_length)/2
    if lface_length < 50 or rface_length < 50: 
        nt=time.time()
        print('not on screeen',int(nt-st))
    return
def midpoint(p1,p2):
    return int((p1.x+p2.x)/2),int((p2.y+p2.y)/2)
st=time.time()
while True:
    ret,frame=cap.read()
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces=detector(gray)
    for points in faces:
        x,y=points.left(),points.top()
        x1,y1=points.right(),points.bottom()
        cv2.rectangle(frame,(x,y),(x1,y1),(0,0,255),2)
        landmark=predictor(gray,points)
        face_movement(landmark)
        eye_gaze(landmark)
    cv2.imshow('frame',frame)
    out.write(frame)
   
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break
cv2.destroyAllWindows()
cap.release()
