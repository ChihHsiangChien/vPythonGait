from vpython import *
import serial  # 引用pySerial模組
import time
    
COM_PORT = 'COM19'    # 指定通訊埠名稱
BAUD_RATES = 115200    # 設定傳輸速率
sensor = serial.Serial(COM_PORT, BAUD_RATES)   # 初始化序列通訊埠



scene.width = 400
scene.height = 600
scene.align = 'left'


"""
產生參考坐標軸
"""
x_axis = cylinder(pos=vector(0,0,0), axis=vector(100,0,0), color = vector(1,0,0), radius=0.5, opacity = .5) #X axis
y_axis = cylinder(pos=vector(0,0,0), axis=vector(0,100,0), color = vector(0,1,0), radius=0.5, opacity = .5) #Y axis
z_axis = cylinder(pos=vector(0,0,0), axis=vector(0,0,100), color = vector(0,0,1), radius=0.5, opacity = .5) #Z axis

                
"""
繪製髖、大腿femur、小腿tibia、腳掌foot
"""
#骨盆setup
pelvis_length = 30 #along x axis
pelvis_width = 20 #along z axis
pelvis_height = 10 #along y axis

pelvis = box(pos = vector(0,0,0),
          length = pelvis_length,
          height = pelvis_width,
          width = pelvis_height,
          color = vector(.3, .4, .5),
          opacity = .8)

#髖關節位置
#left_hip_joint = sphere(pos=vector(pelvis.pos.x + 10 ,0,0),radius=0.5)
left_hip_joint = sphere(pos= pelvis.pos+ .5*pelvis.axis,radius= 5)

#股骨setup
left_femur_radius = 4 
left_femur_length = 35
left_femur_vertical_axis = vector(0,left_femur_length * -1,0)

#產生股骨
left_femur = cylinder(pos = left_hip_joint.pos,
                 axis = left_femur_vertical_axis,
                 color = vector(.9, .9 , .9), radius= left_femur_radius)
#膝關節位置
#print(femur.pos)
left_knee_joint = sphere(pos= left_femur.pos + left_femur.axis,radius = 5,opacity = .9,
                    make_trail=True,trail_color= color.green)


#脛骨setup
left_tibia_radius = 2
left_tibia_length = 35
left_tibia_vertical_axis = vector(0,left_tibia_length*-1,0)

#產生脛骨
left_tibia = cylinder(pos = left_knee_joint.pos,
                 axis = left_tibia_vertical_axis,
                 color = vector(.8,.8,.8), radius= left_tibia_radius)
#踝關節位置

left_ankle_joint = sphere(pos= left_tibia.pos + left_tibia.axis ,radius = 4, opacity = .9,
                     make_trail=True, trail_color= color.blue)
                    #interval=10, retain=50

#腳掌設定
left_foot_radius = 3 #  腳掌寬度
left_foot_length = 25 #  腳掌長度 
left_foot_verticla_axis = vector(0, left_foot_length*-1, 0 )


#產生腳掌
left_foot = cylinder(pos = left_ankle_joint.pos,
                axis = left_foot_verticla_axis,
                color = vector(.7,.7,.7), radius= left_foot_radius, opacity = .7)



#初始角度
pelvis_pitch_angle = 0
pelvis_roll_angle = 0
pelvis_yaw_angle = 0 

left_hip_pitch_angle = 0
left_hip_roll_angle = 0
left_hip_yaw_angle = 0
left_knee_pitch_angle = 0
left_knee_roll_angle = 0
left_knee_yaw_angle = 0
left_ankle_pitch_angle = 0
left_ankle_roll_angle = 0
left_ankle_yaw_angle = 0

#攝影機角度
scene.camera.pos = vector(100,-22, 8)
scene.camera.axis = vector(-91, -26, 0)

#產生角度紀錄圖表
gr = graph(fast=False,
           align='right',
           width=400, height=300,
           title='<b>Leg Angle</b>',
           xtitle='<i>time</i>', ytitle='<b>Angle</b>',
           foreground=color.black, background=color.white,
           xmin = 0, xmax=50, ymin=-45, ymax=180)

hip_angle_curve = gcurve(color = color.red, label = 'hip')
knee_angle_curve = gcurve(color = color.green,label = 'knee')
ankle_angle_curve = gcurve(color = color.blue,label = 'ankle')


i=0

try:
    while True:
        while (sensor.in_waiting):          # 若收到序列資料…
            #print(scene.camera.pos)
            #print(scene.camera.axis)       
              
            data_raw = sensor.readline()    # 讀取一行
            data = data_raw.decode()        # 用預設的UTF-8解碼
            data = data.replace(" ", "")    #去除所有的空白
            data = data.replace("\r\n", "") #去除換行符號
            if len(data) == 0:continue        #如果是空資料則不處理，略過此迴圈
            dataNums=data.split(',')        #將資料以逗號分隔
    
            #sensor_id = int(float(dataNums[0]))
            sensor_id = 0
            
            pitch_angle = int(float(dataNums[1]))
            roll_angle = int(float(dataNums[2]))
            yaw_angle = int(float(dataNums[3]))
            
           
            if sensor_id == 0 :
                pelvis_pitch_angle = 90 - pitch_angle
                pelvis_roll_angle = roll_angle
                pelvis_yaw_angle = 180 - yaw_angle
     
            elif sensor_id == 1 :
                left_hip_pitch_angle = 90 - pitch_angle
                left_hip_roll_angle = roll_angle
                left_hip_yaw_angle = 180 - yaw_angle

            elif sensor_id == 2 :     
                left_knee_pitch_angle = 90 - pitch_angle
                left_knee_roll_angle = roll_angle
                left_knee_yaw_angle = 180 - yaw_angle

            elif sensor_id == 3 :     
                left_ankle_pitch_angle = 90 - pitch_angle
                left_ankle_roll_angle = roll_angle
                left_ankle_yaw_angle = 180 - yaw_angle
                 
            
            pelvis.up = vector(0,pelvis_height,0).rotate(angle = radians( pelvis_pitch_angle ), axis = vector(1,0,0) )
            #pelvis.up = pelvis.up.rotate(angle = radians( pelvis_roll_angle ), axis = vector(0,0,1) )
            pelvis.axis = vector(pelvis_length,0,0).rotate(angle = radians( pelvis_yaw_angle ), axis = vector(0,1,0) )

            left_hip_joint.pos = pelvis.pos + .5*pelvis.axis
            left_femur.pos = left_hip_joint.pos
            left_femur.axis = left_femur_vertical_axis.rotate(angle = radians( left_hip_pitch_angle ), axis = vector(1,0,0) * -1)
            left_femur.axis = left_femur.axis.rotate(angle = radians( left_hip_roll_angle ), axis = vector(0,0,1) )
            left_femur.axis = left_femur.axis.rotate(angle = radians( left_hip_yaw_angle ), axis = vector(0,1,0) )

            left_knee_joint.pos = left_femur.pos + left_femur.axis
            left_tibia.pos = left_knee_joint.pos
            left_tibia.axis = left_tibia_vertical_axis.rotate(angle = radians( left_knee_pitch_angle ), axis = vector(1,0,0) ) #tibia backward
            left_tibia.axis = left_tibia.axis.rotate(angle = radians( left_knee_roll_angle ), axis = vector(0,0,1) )
            left_tibia.axis = left_tibia.axis.rotate(angle = radians( left_knee_yaw_angle ), axis = vector(0,1,0) )

            left_ankle_joint.pos = left_tibia.pos + left_tibia.axis
            left_foot.pos = left_ankle_joint.pos
            left_foot.axis = left_foot_verticla_axis.rotate(angle = radians( left_ankle_pitch_angle ), axis = vector(1,0,0) * -1)
            left_foot.axis = left_foot.axis.rotate(angle = radians( left_ankle_roll_angle ), axis = vector(0,0,1) )
            left_foot.axis = left_foot.axis.rotate(angle = radians( left_ankle_yaw_angle ), axis = vector(0,1,0) )                
        
                    
            #讓圖表能呈現最新的資料點
            if i > gr.xmax:
                d = i-gr.xmax
                gr.xmin += d
                gr.xmax += d
                
            hip_angle_curve.plot( i, left_hip_pitch_angle )
            knee_angle_curve.plot( i, left_knee_pitch_angle )
            ankle_angle_curve.plot( i, left_ankle_pitch_angle )
            
            i += 1

except KeyboardInterrupt:
    sensor.close()    # 清除序列通訊物件
    print('再見！')

