# -*- coding: gbk -*-
from ast import IsNot
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import array
from ctypes.wintypes import MAX_PATH
import serial
import threading
import numpy as np
import time
import pyqtgraph as pg
import keyboard
import os
from graphics import *

i = 0
maxset = 1400
minset = 1300
cutset = 70
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
                mpower = qc[1]
                mpower = mpower[1::2]
                #print(mpower)

                global check_rate
                global num_check
                global time_get
                global minpower
                global maxpower
                global asc
                global flag
                

                asctem=''
                if int(mpower) > maxpower:
                    maxpower = int(mpower) 
                if int(mpower) < minpower:
                    minpower = int(mpower)
                time_end = time.time()
                if time_end - time_get >=0.49999:
                    if  maxpower-minpower > cutset:
                        check_rate = 1
                    if check_rate == 1:
                        num_check=num_check+'1'
                    else:
                        num_check=num_check+'0'
                    #print(maxpower,minpower)
                    check_rate = 0
                    maxpower = 0
                    minpower = 10000
                    os.system('cls') 
                    print(num_check,"����������:")
                    if num_check[-3:]=='111' and flag == 0:
                        flag =  1
                        num_check = ''
                    if len(num_check)%8==0 and flag ==1 and num_check != '':
                        asctem = num_check[(len(num_check)-8):]
                        asc=asc+chr(int(asctem, 2))
                        
                        print(asc,"�յ���Ϣ:")
                        print(time_c,"TIME:")
                    time_get = time_end 
                    time_c= time_end - time_start  
                    #print(time_c,"TIME:")      
                    #print(len(np.nonzero(data)[0]))
                global i;
                if i< historyLength:
                    data[i]=mpower
                    i=i+1
                else: 
                    data[:-1]=data[1:] 
                    data[i-1]=mpower  
 
def plotData():
    curve.setData(data)
 
class Stream(QObject):
    newText = pyqtSignal(str)

    def write(self, text):
        self.newText.emit(str(text))
        QApplication.processEvents()

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.initGui()
        sys.stdout = Stream(newText=self.onUpdateText)
        self.setWindowTitle("�����ʾ")
        
    def initGui(self):
        self.layout = QVBoxLayout()

        self.btn1 = QPushButton('Test')
        self.btn1.clicked.connect(self.printHello)

        self.consoleBox = QTextEdit(self, readOnly=True)

        self.layout.addWidget(self.btn1)
        self.layout.addWidget(self.consoleBox)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)
        self.show()
    def onUpdateText(self, text):
        """Write console output to text widget."""
        cursor = self.consoleBox.textCursor()
        cursor.movePosition(QTextCursor.Start)
        cursor.insertText(text)
        self.consoleBox.setTextCursor(cursor)
        self.consoleBox.ensureCursorVisible()
    def closeEvent(self, event):
        """Shuts down application on close."""
        # Return stdout to defaults.
        sys.stdout = sys.__stdout__
        super().closeEvent(event)
    def printHello(self):
        self.setWindowTitle("�����ʾ")

if __name__ == "__main__":
    num_check=''
    asc=''
    check_rate = 0
    flag = 0
    maxpower = 0
    minpower = 10000
    app = QApplication(sys.argv)
    main = MainWindow()
    app = pg.mkQApp() # ����app
    win = pg.GraphicsWindow() # ��������
    win.setWindowTitle(u'����ͼ')
    win.resize(800, 500) # С���ڴ�С
    data = array.array('i') # �ɶ�̬�ı�����Ĵ�С,double������
    historyLength = 2000 # �����곤��
    a = 0
    data=np.zeros(historyLength).__array__('d')#�����鳤�ȶ�����
    p = win.addPlot() # ��ͼp���뵽������
    p.showGrid(x=True, y=True) # ��X��Y�ı���
    p.setRange(xRange=[0, historyLength], yRange=[1200,1600], padding=0)
    p.setLabel(axis='left', text='y ') # ����
    p.setLabel(axis='bottom', text='x / point')
    p.setTitle('semg') # ��������
    curve = p.plot() # ����һ��ͼ��
    curve.setData(data)
    portx = 'COM6'
    bps = 115200
    # ����ִ�е����Ѿ��� ����open����ᱨ��
    mSerial = serial.Serial(portx, int(bps))
    if (mSerial.isOpen()):
        print("open success")
        mSerial.write("hello".encode()) # ��˿�Щ���� �ַ�����������
        mSerial.flushInput() # ��ջ�����
    else:
        print("open failed")
        serial.close() # �رն˿�
    time_start = time.time()
    time_get = time_start
    th1 = threading.Thread(target=Serial)#Ŀ�꺯��һ�����ܴ�����
    th1.start()
    timer = pg.QtCore.QTimer()
    timer.timeout.connect(plotData) # ��ʱˢ��������ʾ
    timer.start(50) # ����ms����һ��
    app.exec_()






