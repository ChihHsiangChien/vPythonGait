from vpython import *


"""
#Reading Data from serial
import serial
import time

sensorData = serial.serial('com9',9600)
while True:
    while(sensorData.inWaiting()==0):
        pass
    textline = sensorData.readline()
    dataNums=textline.split(',')
    x1 = float(dataNums[0])
    y1 = float(dataNums[1])
    z1 = float(dataNums[2])
    x2 = float(dataNums[3])
    y2 = float(dataNums[4])
    z2 = float(dataNums[5])
    x3 = float(dataNums[6])
    y3 = float(dataNums[7])
    z3 = float(dataNums[8])
"""    
    
"""
基本設定
"""
scale = 0.1 #


"""
產生坐標軸，做為參考用
"""
xaxis = cylinder(pos=vector(0,0,0), axis=vector(10,0,0), color = vector(1,0,0), radius=0.05) #X axis
yaxis = cylinder(pos=vector(0,0,0), axis=vector(0,10,0), color = vector(0,1,0), radius=0.05) #Y axis
Zaxis = cylinder(pos=vector(0,0,0), axis=vector(0,0,10), color = vector(0,0,1), radius=0.05) #Z axis

                
"""
繪製髖、大腿femur、小腿tibia、腳掌foot
"""
#骨盆setup
hip_l = 45 #along x axis
hip_w = 15 #along z axis
hip_h = 20 #along y axis

hip = box(pos = vector(0,0,0),
          length = hip_l*scale,
          height = hip_h*scale,
          width = hip_w*scale,
          color = vector(.3, .4, .5))

#髖關節位置
hip_joint = vector(hip.pos.x + 1 ,0,0)


#股骨setup
femur_radius = 4 
femur_length = 35
femur_vertical_axis = vector(0,femur_length*scale*-1,0)

#產生股骨
femur = cylinder(pos = hip_joint,
                 axis = femur_vertical_axis,
                 color = vector(.5,.5,.5), radius= femur_radius * scale)
#膝關節位置
#print(femur.pos)
knee = femur.pos + femur.axis

#脛骨setup
tibia_radius = 2
tibia_length = 35
tibia_vertical_axis = vector(0,tibia_length*scale*-1,0)

#產生脛骨
tibia = cylinder(pos = knee,
                 axis = tibia_vertical_axis,
                 color = vector(.5,.2,.2), radius= tibia_radius * scale)
#踝關節位置
ankle = tibia.pos + tibia.axis

#腳掌設定
foot_radius = 8 #  腳掌寬度
foot_length = 25 #  腳掌長度 
dist_btw_ankle_midfoot = 7 #踝關節和腳中間的距離
foot_verticla_axis = vector(0, foot_length * scale*-1, 0 )


#產生腳掌
foot = cylinder(pos = ankle,
                axis = foot_verticla_axis,
                color = vector(.5,.2,.2), radius= foot_radius * scale)


#攝影機角度
scene.camera.pos = vector(10,0,5)
scene.camera.axis = scene.camera.pos * -1

i = 0 
while True:
    rate(1)
    
    femur.axis = femur_vertical_axis.rotate(angle = radians( 20 + sin(i)*30 ), axis = proj(hip_joint,vector(1,0,0)) * -1)
    knee = femur.pos + femur.axis
    tibia.pos = knee
    tibia.axis = tibia_vertical_axis.rotate(angle = radians( 40 + sin(i*.5 - 10)*10 ), axis = proj(knee,vector(1,0,0))) #tibia backward
    ankle = tibia.pos + tibia.axis
    
    foot.pos = ankle + vector(0,0,dist_btw_ankle_midfoot*scale)
    #foot.axis = foot_verticla_axis.rotate(angle = radians( sin(i)*30 ), axis = proj(ankle, vector(1,0,0) )*-1)
    #foot.axis = foot_verticla_axis.rotate(angle = radians( sin(i)*30 ), axis = proj(ankle,vector(1,0,0)) *-1)
    i += 1
