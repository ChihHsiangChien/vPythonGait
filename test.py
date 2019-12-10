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

#骨盆setup
pelvis_length = 50 #along x axis
pelvis_width = 30 #along z axis
pelvis_height = 10 #along y axis
pelvis_vertical_axis = vector(0,pelvis_height,0)

pelvis = box(pos = vector(0,0,0),
          length = pelvis_length,
          height = pelvis_height,
          width = pelvis_width,
          up=vector(0,1,0),
          color = vector(.3, .4, .5),
          opacity = .2)

#pelvis_front_axis = pelvis.up.rotate(angle = radians(90), axis = vector(1,0,0))
pelvis_front_axis = cross(pelvis.axis,pelvis.up) 

pelvis_front_pointer = arrow(pos = pelvis.pos, axis = pelvis_front_axis, shaftwidth=2, color = color.white)

pelvis_up_pointer = arrow(pos = pelvis.pos, axis = pelvis.up*20, shaftwidth=2, color = vector(.8, .5, .5))


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
                pelvis_pitch_angle =  -pitch_angle
                pelvis_roll_angle = roll_angle
                pelvis_yaw_angle = -yaw_angle
            
            #pitch  yaw 
            #pelvis.up = vector(0,pelvis_height,0).rotate(angle = radians( pelvis_pitch_angle ), axis = vector(1,0,0))
            #pelvis.axis = vector(pelvis_length,0,0).rotate(angle = radians( pelvis_yaw_angle ), axis = vector(0,1,0))
            
            #roll yaw
            #pelvis.axis = vector(pelvis_length,0,0).rotate(angle = radians( pelvis_roll_angle ), axis =  cross(pelvis.axis,pelvis.up) )
            #pelvis.axis = pelvis.axis.rotate(angle = radians( pelvis_yaw_angle ), axis = vector(0,1,0))
            
            #pitch roll
            pelvis.up = vector(0,pelvis_height,0).rotate(angle = radians( pelvis_pitch_angle ), axis = vector(1,0,0))
            pelvis.axis = vector(pelvis_length,0,0).rotate(angle = radians( pelvis_roll_angle ), axis =  cross(pelvis.axis,pelvis.up) )
            
            pelvis_front_pointer.axis = cross(pelvis.axis,pelvis.up) *.1
            pelvis_up_pointer.axis = pelvis.up 
            
            
            
            
            

except KeyboardInterrupt:
    sensor.close()    # 清除序列通訊物件
    print('再見！')

