import sys
from PyQt5.QtCore import pyqtSlot, QTimer, Qt, QPoint
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.uic import loadUi
from PyQt5 import QtGui
import threading
import time
import json
import socket
# import asyncio # Used for asynchronous functions


class GUI(QMainWindow):
    def __init__(self):
        super(GUI, self).__init__()
        loadUi('gui.ui',self)

        '''Input data into the GUI below
        Modification to the following variables will appear on the GUI instantly
        '''
        self.team_id = '0123456'
        self.end_distance = 1609 #meters
        self.distance = 0 #meters
        self.speed = 0 #MPH
        self.acceleration = 0 #M/S2
        self.state = "STOPPING"
        self.max_battery_temp = 0 #F
        self.vibration = 0 #Hz
        self.voltage12 = 0 #V
        self.packVolt1 = 0 
        self.packAmp1 = 0 #A
        self.packVolt2 = 0
        self.packAmp2 = 0
        self.packVolt3 = 0
        self.packAmp3 = 0
        self.podTimer = 0 #seconds
        self.startTimer = 0 #used to determine the time of a run
        self.timerSwitch = True
        self.launched_yet = False;

        #Title of the entire window
        self.setWindowTitle('Cal Poly Hyperloop')
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setFixedSize(1600, 1200)
        self.teamId.setText("TEAM ID: "+self.team_id)


        #Used to allow GUI to be draggable
        self.oldPos = self.pos()

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint (event.globalPos() - self.oldPos)
        #print(delta)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()


    '''GUI UPDATE FUNCTIONS'''

    def update_distance(self): #This function doesn't need to change
        completion_ratio = self.distance/self.end_distance
        #1400 is the value at which the progress bar and clipart reach the end
        progressRatio = int(1400*completion_ratio)
        self.distanceLabel.setText(str(self.distance)+'M') 
        if progressRatio>1400:
            self.pause_timer()
        else:
            self.podClipArt.move(progressRatio+45,1225-118)
            self.distanceLabel.move(progressRatio+35,1185-118)
            self.progressBar.resize(progressRatio+50, 80);

    def update_speedLabel(self):
        self.speedLabel.setText(str(self.speed))    

    def update_accelerationLabel(self):
        accelerationText = "{0:.3f}".format(self.acceleration)
        self.accele.setText(accelerationText)    

    def update_stateLabel(self):
        self.stateLabel.setText(self.state)    

    def update_batteryTempLabel(self):
        battery_temp_text = "{0:.2f}".format(self.max_battery_temp)
        self.maxBatteryTemp.setText(battery_temp_text+" F°")  

    def update_vibrationLabel(self):
        vibration_text = "{0:.2f}".format(self.vibration)
        self.vibration_label.setText(vibration_text+" Hz")  

    def update_voltage12Label(self):
        voltage12_text = "{0:.2f}".format(self.voltage12)
        self.voltageTwelve.setText(voltage12_text+" V")

    def update_pack1_voltage(self):
        voltage_text = "{0:.2f}".format(self.packVolt1)
        self.V1.setText(voltage_text+" V")

    def update_pack2_voltage(self):
        voltage_text = "{0:.2f}".format(self.packVolt2)
        self.V2.setText(voltage_text+" V")

    def update_pack3_voltage(self):
        voltage_text = "{0:.2f}".format(self.packVolt3)
        self.V3.setText(voltage_text+" V")

    def update_pack1_current(self):
        current_text = "{0:.2f}".format(self.packAmp1)
        self.A1.setText(current_text+" A")        

    def update_pack2_current(self):
        current_text = "{0:.2f}".format(self.packAmp2)
        self.A2.setText(current_text+" A")

    def update_pack3_current(self):
        current_text = "{0:.2f}".format(self.packAmp3)
        self.A3.setText(current_text+" A")

    def update_batteryPack1_Health(self):
        if self.packVolt1 > 20:
            self.warn1.setStyleSheet("QLabel { background-color : red; border-radius: 5px;}");
        elif self.packVolt1> 5:
            self.warn1.setStyleSheet("QLabel { background-color : lime; border-radius: 5px;}");
        else:
            self.warn1.setStyleSheet("QLabel { background-color : yellow; border-radius: 5px;}");

    def update_batteryPack2_Health(self):
        if self.packVolt2 > 20:
            self.warn2.setStyleSheet("QLabel { background-color : red; border-radius: 5px;}");
        elif self.packVolt2> 5:
            self.warn2.setStyleSheet("QLabel { background-color : lime; border-radius: 5px;}");
        else:
            self.warn2.setStyleSheet("QLabel { background-color : yellow; border-radius: 5px;}");

    def update_batteryPack3_Health(self):
        if self.packVolt3 > 20:
            self.warn3.setStyleSheet("QLabel { background-color : red; border-radius: 5px;}");
        elif self.packVolt3> 5:
            self.warn3.setStyleSheet("QLabel { background-color : lime; border-radius: 5px;}");
        else:
            self.warn3.setStyleSheet("QLabel { background-color : yellow; border-radius: 5px;}");

    def update_batteryPacks(self):
        self.update_pack1_voltage()
        self.update_pack2_voltage()
        self.update_pack3_voltage()
        self.update_pack1_current()
        self.update_pack2_current()
        self.update_pack3_current()
        self.update_batteryPack1_Health()
        self.update_batteryPack2_Health()
        self.update_batteryPack3_Health()

    def start_timer(self):
        if self.timerSwitch:
            currentTime = time.time()
            self.podTimer = currentTime - self.startTimer
            time_label = "{0:.3f}".format(self.podTimer)
            self.timer.setText(time_label)       

    def pause_timer(self):
        self.timerSwitch = False

    def clear_timer(self):
        self.podTimer = time.time()
        self.startTimer = self.podTimer
        self.timer.setText("0.000")    
        self.timerSwitch = True  

    def update_error_label(self, message=None):
        '''Pass in nothing to make error message disapear'''
        if message is None:
            self.errors_label.setStyleSheet("QLabel {color: transparent; background: transparent;}");
        else:
            self.errors_label.setText(message) 
            self.errors_label.setStyleSheet("QLabel {color: red; background: transparent;}");


app = QApplication(sys.argv)
widget = GUI()
widget.show()

s = socket.socket()
port = 5001
s.connect(('192.168.0.6', port))
connected = True

widget.startTimer = time.time()
def update_labels():
    global connected
    global s
    '''RECIEVE ALL DATA HERE
    NOTE: currently just simulating data chagnes
    '''
    # RECIEVED_JSON = '{\
    #   "state": "ACCELERATING",\
    #   "acceleration": 5,\
    #   "speed": 30,\
    #   "distance": 10,\
    #   "max_battery_temp": 35,\
    #   "vibration": 22,\
    #   "voltage12V": 22,\
    #   "pack1_volt": 11,\
    #   "pack2_volt": 22,\
    #   "pack3_volt": 33,\
    #   "pack1_Amp": 11,\
    #   "pack2_Amp": 22,\
    #   "pack3_Amp": 33\
    # }'\

    RECIEVED_JSON = s.recv(1024)
    print(RECIEVED_JSON)
    recieved = '{'+RECIEVED_JSON.decode().split('}{')[-1].strip('{')
    print(recieved)

    try:
        data = recieved
        print("DATA _______________________: ",data)
        json_parsed = json.loads(data)
        widget.state = json_parsed["state"]
        # widget.acceleration = json_parsed["acceleration"]
        # widget.speed = json_parsed["speed"]
        widget.distance = json_parsed["distance"]
        # widget.max_battery_temp = json_parsed["max_battery_temp"]
        # widget.vibration = json_parsed["vibration"]
        # widget.voltage12 = json_parsed["voltage12V"]
        # widget.packVolt1 = json_parsed["pack1_volt"]
        # widget.packVolt2 = json_parsed["pack2_volt"]
        # widget.packVolt3 = json_parsed["pack3_volt"]
        # widget.packAmp3 = json_parsed["pack1_Amp"]
        # widget.packAmp2 = json_parsed["pack2_Amp"]
        # widget.packAmp1 = json_parsed["pack3_Amp"]

        '''UPDATE GUI'''
        
        widget.update_speedLabel()
        widget.update_distance()
        widget.update_accelerationLabel()
        widget.update_stateLabel()
        widget.update_batteryTempLabel()
        widget.update_vibrationLabel()
        widget.update_voltage12Label()
        widget.update_batteryPacks()
        widget.update_error_label("ERROR MESSAGE HERE")
        if widget.state.upper() == "LAUNCHING" or widget.launched_yet:
            widget.start_timer()
            widget.launched_yet = True
        elif not widget.launched_yet:
            widget.clear_timer()
    except Exception as e:
        print(e)
        if len(data) < 2:
            connected = False
            s.close()
            s = socket.socket()
            while not connected:
                try: 
                    s.connect(('192.168.0.6', 5001))
                    connected = True
                except socket.error:
                    print("no connection yet")
                    time.sleep(1)
                
timer = QTimer()
timer.timeout.connect(update_labels)
timer.start(20)

sys.exit(app.exec_())


if __name__ == '__main__':
    main()