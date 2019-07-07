import sys
from PyQt5.QtCore import pyqtSlot, QTimer, Qt, QPoint
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.uic import loadUi
from PyQt5 import QtGui
import threading
import time
import json
import socket


class GUI1(QMainWindow):
    def __init__(self):
        super(GUI1, self).__init__()
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

class GUI2(QMainWindow):
    def __init__(self):
        super(GUI2, self).__init__()
        loadUi('gui_2.ui',self)

        '''Input data into the GUI below
        Modification to the following variables will appear on the GUI instantly
        '''

        #BATTERY PACKS (RANGES)
        self.chargeState_minRange = 0;
        self.chargeState_maxRange = 100;
        self.volt_minRange = 40;
        self.volt_maxRange = 72;
        self.curr_minRange = 0;
        self.curr_maxRange = 480;
        self.minCell_minRange = 2;
        self.minCell_maxRange = 3.6;
        self.maxCell_minRange = 2;
        self.maxCell_maxRange = 3.6;
        self.packTemp_minRange = 0;
        self.packTemp_maxRange = 60;

        #PNEUMATICS (RANGES)
        self.brakesPressure_minRange = 240;
        self.brakesPressure_maxRange = 250;
        self.tensionerPressure_minRange = 50;
        self.tensionerPressure_maxRange = 150;
        self.brakesTemprature_minRange = 0;
        self.brakesTemprature_maxRange = 60;

        #12V BATTERY (RANGES)
        self.battery_minRange = 11;
        self.battery_maxRange = 14;

        #MOTOR TEMPRATURE (RANGES)
        self.motorTemp_minRange = 0;
        self.motorTemp_maxRange = 70;

        #FRONT PACK
        self.FP_state_value = 0;
        self.FP_volt_value = 0;
        self.FP_curr_value = 0;
        self.FP_minCell_value = 0;
        self.FP_maxCell_value = 0;
        self.FP_t1_value = 0;
        self.FP_t2_value = 0;
        self.FP_t3_value = 0;
        self.FP_t4_value = 0;
        self.FP_t5_value = 0;
        self.FP_t6_value = 0;
        self.FP_t7_value = 0;
        self.FP_t8_value = 0;

        #MIDDLE PACK
        self.MP_state_value = 0;
        self.MP_volt_value = 0;
        self.MP_curr_value = 0;
        self.MP_minCell_value = 0;
        self.MP_maxCell_value = 0;
        self.MP_t1_value = 0;
        self.MP_t2_value = 0;
        self.MP_t3_value = 0;
        self.MP_t4_value = 0;
        self.MP_t5_value = 0;
        self.MP_t6_value = 0;
        self.MP_t7_value = 0;
        self.MP_t8_value = 0;

        #REAR PACK
        self.RP_state_value = 0;
        self.RP_volt_value = 0;
        self.RP_curr_value = 0;
        self.RP_minCell_value = 0;
        self.RP_maxCell_value = 0;
        self.RP_t1_value = 0;
        self.RP_t2_value = 0;
        self.RP_t3_value = 0;
        self.RP_t4_value = 0;
        self.RP_t5_value = 0;
        self.RP_t6_value = 0;
        self.RP_t7_value = 0;
        self.RP_t8_value = 0;

        #PNEUMATICS
        self.brakes_pressure_value = 0;
        self.tensioner_pressure_value = 0;
        self.brakes_temp_value = 0;

        #12V Battery
        self.battery_actual_value = 0;
        self.battery_min.setText(str(self.battery_minRange)+" V")
        self.battery_max.setText(str(self.battery_maxRange)+" V")

        #motors
        self.TL_rpm_value = 0;
        self.ML_rpm_value = 0;
        self.BL_rpm_value = 0;
        self.TR_rpm_value = 0;
        self.MR_rpm_value = 0;
        self.BR_rpm_value = 0;
        self.TL_temp_value = 0;
        self.ML_temp_value = 0;
        self.BL_temp_value = 0;
        self.TR_temp_value = 0;
        self.MR_temp_value = 0;
        self.BR_temp_value = 0;




        #Title of the entire window
        self.setWindowTitle('Cal Poly Hyperloop')
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setFixedSize(1600, 1200)


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

    def update_frontPack_label(self):
        state_text = "{0:.2f}".format(self.FP_state_value) 
        volt_text = "{0:.2f}".format(self.FP_volt_value) 
        curr_text = "{0:.2f}".format(self.FP_curr_value) 
        minCell_text = "{0:.2f}".format(self.FP_minCell_value) 
        maxCell_text = "{0:.2f}".format(self.FP_maxCell_value)
        t1_text = "{0:.2f}".format(self.FP_t1_value) 
        t2_text = "{0:.2f}".format(self.FP_t2_value) 
        t3_text = "{0:.2f}".format(self.FP_t3_value) 
        t4_text = "{0:.2f}".format(self.FP_t4_value) 
        t5_text = "{0:.2f}".format(self.FP_t5_value) 
        t6_text = "{0:.2f}".format(self.FP_t6_value) 
        t7_text = "{0:.2f}".format(self.FP_t7_value) 
        t8_text = "{0:.2f}".format(self.FP_t8_value) 

        self.FP_state.setText(state_text+"")
        self.FP_volt.setText(volt_text+" V")
        self.FP_curr.setText(curr_text+" A")
        self.FP_minCell.setText(minCell_text+" V")
        self.FP_maxCell.setText(maxCell_text+" V")
        self.FP_t1.setText(t1_text+" C")
        self.FP_t2.setText(t2_text+" C")
        self.FP_t3.setText(t3_text+" C")
        self.FP_t4.setText(t4_text+" C")
        self.FP_t5.setText(t5_text+" C")
        self.FP_t6.setText(t6_text+" C")
        self.FP_t7.setText(t7_text+" C")
        self.FP_t8.setText(t8_text+" C")

        if self.chargeState_minRange < self.FP_state_value < self.chargeState_maxRange:
            self.FP_state.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.FP_state.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

        if self.volt_minRange < self.FP_volt_value < self.volt_maxRange:
            self.FP_podSquare.setStyleSheet("QLabel { background-color : #00a34f;}");
            self.FP_volt.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.FP_podSquare.setStyleSheet("QLabel { background-color : #9d0b0f;}");
            self.FP_volt.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

        if self.curr_minRange < self.FP_curr_value < self.curr_maxRange:
            self.FP_curr.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.FP_curr.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

        if self.minCell_minRange < self.FP_minCell_value < self.minCell_maxRange:
            self.FP_minCell.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.FP_minCell.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

        if self.maxCell_minRange < self.FP_maxCell_value < self.maxCell_maxRange:
            self.FP_maxCell.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.FP_maxCell.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

        if self.packTemp_minRange < self.FP_t1_value < self.packTemp_maxRange:
            self.FP_t1.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.FP_t1.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

        if self.packTemp_minRange < self.FP_t2_value < self.packTemp_maxRange:
            self.FP_t2.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.FP_t2.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

        if self.packTemp_minRange < self.FP_t3_value < self.packTemp_maxRange:
            self.FP_t3.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.FP_t3.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

        if self.packTemp_minRange < self.FP_t4_value < self.packTemp_maxRange:
            self.FP_t4.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.FP_t4.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

        if self.packTemp_minRange < self.FP_t5_value < self.packTemp_maxRange:
            self.FP_t5.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.FP_t5.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

        if self.packTemp_minRange < self.FP_t6_value < self.packTemp_maxRange:
            self.FP_t6.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.FP_t6.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

        if self.packTemp_minRange < self.FP_t7_value < self.packTemp_maxRange:
            self.FP_t7.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.FP_t7.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

        if self.packTemp_minRange < self.FP_t8_value < self.packTemp_maxRange:
            self.FP_t8.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.FP_t8.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

    def update_middlePack_label(self):
        state_text = "{0:.2f}".format(self.MP_state_value) 
        volt_text = "{0:.2f}".format(self.MP_volt_value) 
        curr_text = "{0:.2f}".format(self.MP_curr_value) 
        minCell_text = "{0:.2f}".format(self.MP_minCell_value) 
        maxCell_text = "{0:.2f}".format(self.MP_maxCell_value)
        t1_text = "{0:.2f}".format(self.MP_t1_value) 
        t2_text = "{0:.2f}".format(self.MP_t2_value) 
        t3_text = "{0:.2f}".format(self.MP_t3_value) 
        t4_text = "{0:.2f}".format(self.MP_t4_value) 
        t5_text = "{0:.2f}".format(self.MP_t5_value) 
        t6_text = "{0:.2f}".format(self.MP_t6_value) 
        t7_text = "{0:.2f}".format(self.MP_t7_value) 
        t8_text = "{0:.2f}".format(self.MP_t8_value) 

        self.MP_state.setText(state_text+"")
        self.MP_volt.setText(volt_text+" V")
        self.MP_curr.setText(curr_text+" A")
        self.MP_minCell.setText(minCell_text+" V")
        self.MP_maxCell.setText(maxCell_text+" V")
        self.MP_t1.setText(t1_text+" C")
        self.MP_t2.setText(t2_text+" C")
        self.MP_t3.setText(t3_text+" C")
        self.MP_t4.setText(t4_text+" C")
        self.MP_t5.setText(t5_text+" C")
        self.MP_t6.setText(t6_text+" C")
        self.MP_t7.setText(t7_text+" C")
        self.MP_t8.setText(t8_text+" C")

        if self.chargeState_minRange < self.MP_state_value < self.chargeState_maxRange:
            self.MP_state.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.MP_state.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

        if self.volt_minRange < self.MP_volt_value < self.volt_maxRange:
            self.MP_podSquare.setStyleSheet("QLabel { background-color : #00a34f;}");
            self.MP_volt.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.MP_podSquare.setStyleSheet("QLabel { background-color : #9d0b0f;}");
            self.MP_volt.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

        if self.curr_minRange < self.MP_curr_value < self.curr_maxRange:
            self.MP_curr.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.MP_curr.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

        if self.minCell_minRange < self.MP_minCell_value < self.minCell_maxRange:
            self.MP_minCell.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.MP_minCell.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

        if self.maxCell_minRange < self.MP_maxCell_value < self.maxCell_maxRange:
            self.MP_maxCell.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.MP_maxCell.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

        if self.packTemp_minRange < self.MP_t1_value < self.packTemp_maxRange:
            self.MP_t1.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.MP_t1.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

        if self.packTemp_minRange < self.MP_t2_value < self.packTemp_maxRange:
            self.MP_t2.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.MP_t2.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

        if self.packTemp_minRange < self.MP_t3_value < self.packTemp_maxRange:
            self.MP_t3.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.MP_t3.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

        if self.packTemp_minRange < self.MP_t4_value < self.packTemp_maxRange:
            self.MP_t4.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.MP_t4.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

        if self.packTemp_minRange < self.MP_t5_value < self.packTemp_maxRange:
            self.MP_t5.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.MP_t5.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

        if self.packTemp_minRange < self.MP_t6_value < self.packTemp_maxRange:
            self.MP_t6.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.MP_t6.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

        if self.packTemp_minRange < self.MP_t7_value < self.packTemp_maxRange:
            self.MP_t7.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.MP_t7.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

        if self.packTemp_minRange < self.MP_t8_value < self.packTemp_maxRange:
            self.MP_t8.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.MP_t8.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

    def update_rearPack_label(self):
        state_text = "{0:.2f}".format(self.RP_state_value) 
        volt_text = "{0:.2f}".format(self.RP_volt_value) 
        curr_text = "{0:.2f}".format(self.RP_curr_value) 
        minCell_text = "{0:.2f}".format(self.RP_minCell_value) 
        maxCell_text = "{0:.2f}".format(self.RP_maxCell_value)
        t1_text = "{0:.2f}".format(self.RP_t1_value) 
        t2_text = "{0:.2f}".format(self.RP_t2_value) 
        t3_text = "{0:.2f}".format(self.RP_t3_value) 
        t4_text = "{0:.2f}".format(self.RP_t4_value) 
        t5_text = "{0:.2f}".format(self.RP_t5_value) 
        t6_text = "{0:.2f}".format(self.RP_t6_value) 
        t7_text = "{0:.2f}".format(self.RP_t7_value) 
        t8_text = "{0:.2f}".format(self.RP_t8_value) 

        self.RP_state.setText(state_text+"")
        self.RP_volt.setText(volt_text+" V")
        self.RP_curr.setText(curr_text+" A")
        self.RP_minCell.setText(minCell_text+" V")
        self.RP_maxCell.setText(maxCell_text+" V")
        self.RP_t1.setText(t1_text+" C")
        self.RP_t2.setText(t2_text+" C")
        self.RP_t3.setText(t3_text+" C")
        self.RP_t4.setText(t4_text+" C")
        self.RP_t5.setText(t5_text+" C")
        self.RP_t6.setText(t6_text+" C")
        self.RP_t7.setText(t7_text+" C")
        self.RP_t8.setText(t8_text+" C")

        if self.chargeState_minRange < self.RP_state_value < self.chargeState_maxRange:
            self.RP_state.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.RP_state.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

        if self.volt_minRange < self.RP_volt_value < self.volt_maxRange:
            self.RP_podSquare.setStyleSheet("QLabel { background-color : #00a34f;}");
            self.RP_volt.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.RP_podSquare.setStyleSheet("QLabel { background-color : #9d0b0f;}");
            self.RP_volt.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

        if self.curr_minRange < self.RP_curr_value < self.curr_maxRange:
            self.RP_curr.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.RP_curr.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

        if self.minCell_minRange < self.RP_minCell_value < self.minCell_maxRange:
            self.RP_minCell.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.RP_minCell.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

        if self.maxCell_minRange < self.RP_maxCell_value < self.maxCell_maxRange:
            self.RP_maxCell.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.RP_maxCell.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

        if self.packTemp_minRange < self.RP_t1_value < self.packTemp_maxRange:
            self.RP_t1.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.RP_t1.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

        if self.packTemp_minRange < self.RP_t2_value < self.packTemp_maxRange:
            self.RP_t2.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.RP_t2.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

        if self.packTemp_minRange < self.RP_t3_value < self.packTemp_maxRange:
            self.RP_t3.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.RP_t3.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

        if self.packTemp_minRange < self.RP_t4_value < self.packTemp_maxRange:
            self.RP_t4.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.RP_t4.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

        if self.packTemp_minRange < self.RP_t5_value < self.packTemp_maxRange:
            self.RP_t5.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.RP_t5.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

        if self.packTemp_minRange < self.RP_t6_value < self.packTemp_maxRange:
            self.RP_t6.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.RP_t6.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

        if self.packTemp_minRange < self.RP_t7_value < self.packTemp_maxRange:
            self.RP_t7.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.RP_t7.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

        if self.packTemp_minRange < self.RP_t8_value < self.packTemp_maxRange:
            self.RP_t8.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.RP_t8.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

    def update_pneumatics_label(self):
        brakes_pressure = "{0:.2f}".format(self.brakes_pressure_value) 
        tensioner_pressure = "{0:.2f}".format(self.tensioner_pressure_value) 
        brakes_temp = "{0:.2f}".format(self.brakes_temp_value) 

        self.brakes_pressure.setText(brakes_pressure+" PSI")
        self.tensioner_pressure.setText(tensioner_pressure+" PSI")
        self.brake_temprature.setText(brakes_temp+" C")

        if self.brakesPressure_minRange < self.brakes_pressure_value < self.brakesPressure_maxRange:
            self.brakes_pressure.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.brakes_pressure.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

        if self.tensionerPressure_minRange < self.tensioner_pressure_value < self.tensionerPressure_maxRange:
            self.tensioner_pressure.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.tensioner_pressure.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

        if self.brakesTemprature_minRange < self.brakes_temp_value < self.brakesTemprature_maxRange:
            self.brake_temprature.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.brake_temprature.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

    def update_12Vbattery_label(self):
        voltage = "{0:.2f}".format(self.battery_actual_value) 

        self.battery_actual.setText(voltage+" V")

        if self.battery_minRange < self.battery_actual_value < self.battery_maxRange:
            self.battery_actual.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.battery_actual.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

    def update_motors_label(self):
        top_left_rpm = "{0:.2f}".format(self.TL_rpm_value) 
        top_right_rpm = "{0:.2f}".format(self.TR_rpm_value) 
        middle_left_rpm = "{0:.2f}".format(self.ML_rpm_value) 
        middle_right_rpm = "{0:.2f}".format(self.MR_rpm_value) 
        bottom_left_rpm = "{0:.2f}".format(self.BL_rpm_value) 
        bottom_right_rpm = "{0:.2f}".format(self.BR_rpm_value) 
        top_left_temp = "{0:.2f}".format(self.TL_temp_value) 
        top_right_temp = "{0:.2f}".format(self.TR_temp_value) 
        middle_left_temp = "{0:.2f}".format(self.ML_temp_value) 
        middle_right_temp = "{0:.2f}".format(self.MR_temp_value) 
        bottom_left_temp = "{0:.2f}".format(self.BL_temp_value) 
        bottom_right_temp = "{0:.2f}".format(self.BR_temp_value)

        self.TL_rpm.setText(top_left_rpm+" RPM")
        self.TR_rpm.setText(top_right_rpm+" RPM")
        self.ML_rpm.setText(middle_left_rpm+" RPM")
        self.MR_rpm.setText(middle_right_rpm+" RPM")
        self.BL_rpm.setText(bottom_left_rpm+" RPM")
        self.BR_rpm.setText(bottom_right_rpm+" RPM")
        self.TL_temp.setText(top_left_temp+" C")
        self.TR_temp.setText(top_right_temp+" C")
        self.ML_temp.setText(middle_left_temp+" C")
        self.MR_temp.setText(middle_right_temp+" C")
        self.BL_temp.setText(bottom_left_temp+" C")
        self.BR_temp.setText(bottom_right_temp+" C")

        if self.motorTemp_minRange < self.TL_temp_value < self.motorTemp_maxRange:
            self.TL_tempCircle.setStyleSheet("QLabel {background:rgba(57, 181, 74, .5); border-radius: 22;}");
        else:
            self.TL_tempCircle.setStyleSheet("QLabel {background:rgba(239, 15, 15, 0.5); border-radius: 22;}");

        if self.motorTemp_minRange < self.TR_temp_value < self.motorTemp_maxRange:
            self.TR_tempCircle.setStyleSheet("QLabel {background:rgba(57, 181, 74, .5); border-radius: 22;}");
        else:
            self.TR_tempCircle.setStyleSheet("QLabel {background:rgba(239, 15, 15, 0.5); border-radius: 22;}");

        if self.motorTemp_minRange < self.ML_temp_value < self.motorTemp_maxRange:
            self.ML_tempCircle.setStyleSheet("QLabel {background:rgba(57, 181, 74, .5); border-radius: 22;}");
        else:
            self.ML_tempCircle.setStyleSheet("QLabel {background:rgba(239, 15, 15, 0.5); border-radius: 22;}");

        if self.motorTemp_minRange < self.MR_temp_value < self.motorTemp_maxRange:
            self.MR_tempCircle.setStyleSheet("QLabel {background:rgba(57, 181, 74, .5); border-radius: 22;}");
        else:
            self.MR_tempCircle.setStyleSheet("QLabel {background:rgba(239, 15, 15, 0.5); border-radius: 22;}");

        if self.motorTemp_minRange < self.BL_temp_value < self.motorTemp_maxRange:
            self.BL_tempCircle.setStyleSheet("QLabel {background:rgba(57, 181, 74, .5); border-radius: 22;}");
        else:
            self.BL_tempCircle.setStyleSheet("QLabel {background:rgba(239, 15, 15, 0.5); border-radius: 22;}");

        if self.motorTemp_minRange < self.BR_temp_value < self.motorTemp_maxRange:
            self.BR_tempCircle.setStyleSheet("QLabel {background:rgba(57, 181, 74, .5); border-radius: 22;}");
        else:
            self.BR_tempCircle.setStyleSheet("QLabel {background:rgba(239, 15, 15, 0.5); border-radius: 22;}");

    def update_error_label(self, message=None):
        '''Pass in nothing to make error message disapear'''
        if message is None:
            self.errors_label.setStyleSheet("QLabel {color: transparent; background: transparent;}");
        else:
            self.errors_label.setText(message) 
            self.errors_label.setStyleSheet("QLabel {color: red; background: transparent;}");

app = QApplication(sys.argv)
widget1 = GUI1()
widget1.show()
widget2 = GUI2()
widget2.show()

s = socket.socket()
port = 5001
s.connect(('192.168.0.6', port))
connected = True

widget1.startTimer = time.time()
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


        '''UPDATE DATA _SCREEN 1'''
        widget1.state = json_parsed["state"]
        # widget1.acceleration = json_parsed["acceleration"]
        # widget1.speed = json_parsed["speed"]
        widget1.distance = json_parsed["distance"]
        # widget1.max_battery_temp = json_parsed["max_battery_temp"]
        # widget1.vibration = json_parsed["vibration"]
        # widget1.voltage12 = json_parsed["voltage12V"]
        # widget1.packVolt1 = json_parsed["pack1_volt"]
        # widget1.packVolt2 = json_parsed["pack2_volt"]
        # widget1.packVolt3 = json_parsed["pack3_volt"]
        # widget1.packAmp3 = json_parsed["pack1_Amp"]
        # widget1.packAmp2 = json_parsed["pack2_Amp"]
        # widget1.packAmp1 = json_parsed["pack3_Amp"]
        '''UPDATE DATA _SCREEN 1'''
        #FRONT PACK
        widget2.FP_state_value += .1;
        widget2.FP_volt_value += .1;
        widget2.FP_curr_value += .1;
        widget2.FP_minCell_value += .1;
        widget2.FP_maxCell_value += .1;
        widget2.FP_t1_value += .1;
        widget2.FP_t2_value += .1;
        widget2.FP_t3_value += .1;
        widget2.FP_t4_value += .1;
        widget2.FP_t5_value += .1;
        widget2.FP_t6_value += .1;
        widget2.FP_t7_value += .1;
        widget2.FP_t8_value += .1;
        #FRONT PACK
        widget2.MP_state_value += .1;
        widget2.MP_volt_value += .1;
        widget2.MP_curr_value += .1;
        widget2.MP_minCell_value += .1;
        widget2.MP_maxCell_value += .1;
        widget2.MP_t1_value += .1;
        widget2.MP_t2_value += .1;
        widget2.MP_t3_value += .1;
        widget2.MP_t4_value += .1;
        widget2.MP_t5_value += .1;
        widget2.MP_t6_value += .1;
        widget2.MP_t7_value += .1;
        widget2.MP_t8_value += .1;
        #FRONT PACK
        widget2.RP_state_value += .1;
        widget2.RP_volt_value += .1;
        widget2.RP_curr_value += .1;
        widget2.RP_minCell_value += .1;
        widget2.RP_maxCell_value += .1;
        widget2.RP_t1_value += .1;
        widget2.RP_t2_value += .1;
        widget2.RP_t3_value += .1;
        widget2.RP_t4_value += .1;
        widget2.RP_t5_value += .1;
        widget2.RP_t6_value += .1;
        widget2.RP_t7_value += .1;
        widget2.RP_t8_value += .1;
        #PNEUMATICS
        widget2.brakes_pressure_value += .1;
        widget2.tensioner_pressure_value += .1;
        widget2.brakes_temp_value += .1;    
        #12V Battery
        widget2.battery_actual_value += .1;
        #motors
        widget2.TL_rpm_value += .1;
        widget2.ML_rpm_value += .1;
        widget2.BL_rpm_value += .1;
        widget2.TR_rpm_value += .1;
        widget2.MR_rpm_value += .1;
        widget2.BR_rpm_value += .1;
        widget2.TL_temp_value += .1;
        widget2.ML_temp_value += .1;
        widget2.BL_temp_value += .1;
        widget2.TR_temp_value += .1;
        widget2.MR_temp_value += .1;
        widget2.BR_temp_value += .1;


        '''UPDATE GUI _SCREEN 1'''
        widget1.update_speedLabel()
        widget1.update_distance()
        widget1.update_accelerationLabel()
        widget1.update_stateLabel()
        widget1.update_batteryTempLabel()
        widget1.update_vibrationLabel()
        widget1.update_voltage12Label()
        widget1.update_batteryPacks()
        widget1.update_error_label("ERROR MESSAGE HERE")
        '''UPDATE GUI _SCREEN 2'''
        widget2.update_frontPack_label()
        widget2.update_middlePack_label()
        widget2.update_rearPack_label()
        widget2.update_pneumatics_label()
        widget2.update_12Vbattery_label()
        widget2.update_motors_label()
        widget2.update_error_label("ERROR MESSAGE HERE")

        if widget1.state.upper() == "LAUNCHING" or widget1.launched_yet:
            widget1.start_timer()
            widget1.launched_yet = True
        elif not widget1.launched_yet:
            widget1.clear_timer()
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