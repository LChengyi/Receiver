import array
from ctypes.wintypes import MAX_PATH
import serial
import threading
import numpy as np
import time
import pyqtgraph as pg
import keyboard

i = 0
maxset = 1300
minset = 1200
cutset = 200
def Serial():
    while True:
        re = mSerial.readline().hex()
        if keyboard.is_pressed('q'):  # if key 'q' is pressed 
            input("Press Enter to continue...")
            print('continue...')
        if(re[-4:]=='0d0a'):
            re=re[0:-4]
            qc=re.split("2c")
            if(len(qc)==8):
                mpower = qc[6]
                mpower = mpower[1::2]
                #print(mpower)

                global check_rate
                global num_check
                global time_get
                global minpower
                global maxpower
                global asc
                global flag
                time_end = time.time()

        
                if int(mpower) > maxpower:
                    maxpower = int(mpower) 
                if int(mpower) < minpower:
                    minpower = int(mpower)

                if time_end - time_get >=1.9998:
                    if maxpower > maxset and minpower < minset and maxpower-minpower > cutset:
                        check_rate = 1
                    if check_rate == 1:
                        num_check=num_check+'1'
                    else:
                        num_check=num_check+'0'
                    print(maxpower,minpower)
                    check_rate = 0
                    maxpower = 0
                    minpower = 10000
                    print("当前收到的二进制码流:",num_check)
                    if num_check[-3:]=='111' and flag == 0:
                        flag =  1
                        num_check =''
                    if len(num_check)%8==0 and flag ==1:
                        asctem = num_check[(len(num_check)-8):]
                        asc=asc+chr(int(asctem, 2))
                        print("收到信息:",asc)
                    time_get = time_end 
                    time_c= time_end - time_start  
                    print("TIME:",time_c)        
                global i;
                if i< historyLength:
                    data[i]=mpower
                    i=i+1
                else: 
                    data[:-1]=data[1:] 
                    data[i-1]=mpower  
 
def plotData():
    curve.setData(data)
 
 
if __name__ == "__main__":
    num_check=''
    asc=''
    check_rate = 0
    flag = 0
    maxpower = 0
    minpower = 10000
    app = pg.mkQApp() # 建立app
    win = pg.GraphicsWindow() # 建立窗口
    win.setWindowTitle(u'波形图')
    win.resize(800, 500) # 小窗口大小
    data = array.array('i') # 可动态改变数组的大小,double型数组
    historyLength = 2000 # 横坐标长度
    a = 0
    data=np.zeros(historyLength).__array__('d')#把数组长度定下来
    p = win.addPlot() # 把图p加入到窗口中
    p.showGrid(x=True, y=True) # 把X和Y的表格打开
    p.setRange(xRange=[0, historyLength], yRange=[0,300], padding=0)
    p.setLabel(axis='left', text='y / V') # 靠左
    p.setLabel(axis='bottom', text='x / point')
    p.setTitle('semg') # 表格的名字
    curve = p.plot() # 绘制一个图形
    curve.setData(data)
    portx = 'COM3'
    bps = 115200
    # 串口执行到这已经打开 再用open命令会报错
    mSerial = serial.Serial(portx, int(bps))
    if (mSerial.isOpen()):
        print("open success")
        mSerial.write("hello".encode()) # 向端口些数据 字符串必须译码
        mSerial.flushInput() # 清空缓冲区
    else:
        print("open failed")
        serial.close() # 关闭端口
    time_start = time.time()
    time_get = time_start
    th1 = threading.Thread(target=Serial)#目标函数一定不能带（）
    th1.start()
    timer = pg.QtCore.QTimer()
    timer.timeout.connect(plotData) # 定时刷新数据显示
    timer.start(50) # 多少ms调用一次
    app.exec_()

