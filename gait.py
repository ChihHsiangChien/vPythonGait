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
    
#縮小比例
scale = 0.1 #

"""
產生參考坐標軸
"""
xaxis = cylinder(pos=vector(0,0,0), axis=vector(10,0,0), color = vector(1,0,0), radius=0.05, opacity = .5) #X axis
yaxis = cylinder(pos=vector(0,0,0), axis=vector(0,10,0), color = vector(0,1,0), radius=0.05, opacity = .5) #Y axis
Zaxis = cylinder(pos=vector(0,0,0), axis=vector(0,0,10), color = vector(0,0,1), radius=0.05, opacity = .5) #Z axis

                
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
          color = vector(.3, .4, .5),
          opacity = .2)

#髖關節位置
hip_joint = sphere(pos=vector(hip.pos.x + 1 ,0,0),radius=0.5)


#股骨setup
femur_radius = 4 
femur_length = 35
femur_vertical_axis = vector(0,femur_length*scale*-1,0)

#產生股骨
femur = cylinder(pos = hip_joint.pos,
                 axis = femur_vertical_axis,
                 color = vector(.5,.5,.5), radius= femur_radius * scale)
#膝關節位置
#print(femur.pos)
knee_joint = sphere(pos= femur.pos + femur.axis,radius = 0.5,opacity = .9,
                    make_trail=True,trail_color= color.green)


#脛骨setup
tibia_radius = 2
tibia_length = 35
tibia_vertical_axis = vector(0,tibia_length*scale*-1,0)

#產生脛骨
tibia = cylinder(pos = knee_joint.pos,
                 axis = tibia_vertical_axis,
                 color = vector(.5,.2,.2), radius= tibia_radius * scale)
#踝關節位置

ankle_joint = sphere(pos= tibia.pos + tibia.axis ,radius = 0.4, opacity = .9,
                     make_trail=True, trail_color= color.blue)
                    #interval=10, retain=50

#腳掌設定
foot_radius = 3 #  腳掌寬度
foot_length = 25 #  腳掌長度 
dist_btw_ankle_midfoot = 7 #踝關節和腳中間的距離
foot_verticla_axis = vector(0, foot_length * scale*-1, 0 )


#產生腳掌
foot = cylinder(pos = ankle_joint.pos,
                axis = foot_verticla_axis,
                color = vector(.2,.8,.2), radius= foot_radius * scale, opacity = .7)


#攝影機角度
scene.camera.pos = vector(20,0,0)
scene.camera.axis = scene.camera.pos * -1


#產生角度紀錄圖表
gr = graph(fast=False,
           width=600, height=250,
           title='<b>Leg Angle</b>',
           xtitle='<i>time</i>', ytitle='<i>Angle</i>',
           foreground=color.black, background=color.white,
           xmin = 0, xmax=50, ymin=-45, ymax=180)

hip_angle_curve = gcurve(color = color.red, label='hip')
knee_angle_curve = gcurve(color = color.green,label='knee')
ankle_angle_curve = gcurve(color = color.blue,label='ankle')


i = 0 
while True:
    rate(5)
    
    hip_angle = 20 + sin(i)*30
    knee_angle = 40 + sin(i*.5 - 10)*10  
    ankle_angle = 90 + sin(i)*10
    """
    femur_angle = 0
    tibia_angle = 90
    foot_angle = 0
    """                
    femur.axis = femur_vertical_axis.rotate(angle = radians( hip_angle ), axis = vector(1,0,0) * -1)
    #hip_arraw = arrow(pos=hip_joint.pos, axis= vector(5,0,0), shaftwidth=.3)
   
    knee_joint.pos = femur.pos + femur.axis
    
    tibia.pos = knee_joint.pos
    tibia.axis = tibia_vertical_axis.rotate(angle = radians(knee_angle  ), axis = vector(5,0,0) ) #tibia backward
    #knee_arraw = arrow(pos=knee_joint.pos, axis= vector(5,0,0), shaftwidth=.1 , opacity = .2)
                                           
    ankle_joint.pos = tibia.pos + tibia.axis
    
    foot.pos = ankle_joint.pos
    foot.axis = foot_verticla_axis.rotate(angle = radians( ankle_angle ), axis = vector(1,0,0)*-1)
    #ankle_arraw = arrow(pos=ankle_joint.pos, axis= vector(5,0,0), shaftwidth=.1 ,opacity = .3)
    
    #讓圖表能呈現最新的資料點
    if i > gr.xmax:
        d = i-gr.xmax
        gr.xmin += d
        gr.xmax += d
        
    hip_angle_curve.plot( i, hip_angle )
    knee_angle_curve.plot( i, knee_angle )
    ankle_angle_curve.plot( i, ankle_angle )
    
    i += 1