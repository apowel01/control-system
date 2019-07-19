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
        self.team_id = 'SLOLOOP'
        self.end_distance = 125000 #meters
        self.distance = 0 #meters
        self.speed = 0 #MPH
        self.acceleration = 0 #M/S2
        self.state = "STOPPING"
        self.podTimer = 0 #seconds
        self.startTimer = 0 #used to determine the time of a run
        self.timerSwitch = True
        self.launched_yet = False;

        #Title of the entire window
        self.setWindowTitle('Cal Poly Hyperloop')
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setFixedSize(1600, 1200)
        self.move(1920, 0) #MOVE GUI TO FIRST SCREEN

        self.teamId.setText("TEAM ID: "+self.team_id)


        #Used to allow GUI to be draggable
        self.oldPos = self.pos()

    # def mousePressEvent(self, event):
    #     self.oldPos = event.globalPos()

    # def mouseMoveEvent(self, event):
    #     delta = QPoint (event.globalPos() - self.oldPos)
    #     self.move(self.x() + delta.x(), self.y() + delta.y())
    #     self.oldPos = event.globalPos()

    '''GUI UPDATE FUNCTIONS'''

    def update_distance(self): #This function doesn't need to change
        completion_ratio = self.distance/self.end_distance
        #1400 is the value at which the progress bar and clipart reach the end
        progressRatio = int(1400*completion_ratio)
        self.distanceLabel.setText(str(self.distance)+'CM') 
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

class cells_window(QMainWindow):
    def __init__(self, parent):
        super(cells_window, self).__init__(parent)
        loadUi('cells.ui',self)

        self.FP_cells = [0]*20
        self.RP_cells = [0]*20

        self.FP_text = [self.FP_cv1,self.FP_cv2,self.FP_cv3,self.FP_cv4,self.FP_cv5,self.FP_cv6,self.FP_cv7,self.FP_cv8,self.FP_cv9,self.FP_cv10,self.FP_cv11,self.FP_cv12,self.FP_cv13,self.FP_cv14,self.FP_cv15,self.FP_cv16,self.FP_cv17,self.FP_cv18,self.FP_cv19,self.FP_cv20]
        self.RP_text = [self.RP_cv1,self.RP_cv2,self.RP_cv3,self.RP_cv4,self.RP_cv5,self.RP_cv6,self.RP_cv7,self.RP_cv8,self.RP_cv9,self.RP_cv10,self.RP_cv11,self.RP_cv12,self.RP_cv13,self.RP_cv14,self.RP_cv15,self.RP_cv16,self.RP_cv17,self.RP_cv18,self.RP_cv19,self.RP_cv20]
        
        self.setWindowTitle('Cal Poly Hyperloop')
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.move(1050, 0)


        self.hide.clicked.connect(self.on_hide)

    def on_hide(self):
        self.close()
        # for cell in range(len(batteryCells)):

    def update_cells(self):
        for cell in range(len(self.FP_cells)):
            text = "{0:.2f}".format(self.FP_cells[cell])
            self.FP_text[cell].setText(text+" V")
            if 2 < self.FP_cells[cell] < 3.6:
                self.FP_text[cell].setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
            else:
                self.FP_text[cell].setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

        for cell in range(len(self.FP_cells)):
            text = "{0:.2f}".format(self.RP_cells[cell])
            self.RP_text[cell].setText(text+" V")
            if 2 < self.RP_cells[cell] < 3.6:
                self.RP_text[cell].setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
            else:
                self.RP_text[cell].setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

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
        self.Temp_minRange = -20
        self.Temp_maxRange = 60


        #PNEUMATICS (RANGES)
        self.brakesPressure_minRange = 240;
        self.brakesPressure_maxRange = 250;
        self.tensionerPressure_minRange = 80;
        self.tensionerPressure_maxRange = 90;
        self.breaksAirTank_minRange = 0;
        self.breaksAirTank_maxRange = 130;
        self.tensionerAirTank_minRange = 0;
        self.tensionerAirTank_maxRange = 130;
        self.solenoid_minRange = 0;
        self.solenoid_maxRange = 122;
        self.frontTensioner_minRange = 23;
        self.frontTensioner_maxRange = 140;
        self.rearTensioner_minRange = 23;
        self.rearTensioner_maxRange = 140;

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
        self.FP_lowTemp_Value = 0;
        self.FP_avgTemp_Value = 0;
        self.FP_highTemp_Value = 0;
        self.FP_minCell_value = 0;
        self.FP_maxCell_value = 0;
        # self.FP_cell1 = 0;
        # self.FP_cell2 = 0;
        # self.FP_cell3 = 0;
        # self.FP_cell4 = 0;
        # self.FP_cell5 = 0;
        # self.FP_cell6 = 0;
        # self.FP_cell7 = 0;
        # self.FP_cell8 = 0;
        self.FP_isolator_value=0;

        #REAR PACK
        self.RP_state_value = 0;
        self.RP_volt_value = 0;
        self.RP_curr_value = 0;
        self.RP_lowTemp_Value = 0;
        self.RP_avgTemp_Value = 0;
        self.RP_highTemp_Value = 0;        
        self.RP_minCell_value = 0;
        self.RP_maxCell_value = 0;
        # self.RP_cell1 = 0;
        # self.RP_cell2 = 0;
        # self.RP_cell3 = 0;
        # self.RP_cell4 = 0;
        # self.RP_cell5 = 0;
        # self.RP_cell6 = 0;
        # self.RP_cell7 = 0;
        # self.RP_cell8 = 0;
        self.RP_isolator_value=1;

        #PNEUMATICS
        self.brakes_pressure_value = 0;
        self.tensioner_pressure_value = 0;
        self.brakes_airTank_temp_value = 0;
        self.tensioner_airTank_temp_value = 0;
        self.solenoid_temp_value = 0;
        self.frontTensioner__temp_value = 0;
        self.rearTensioner__temp_value = 0;

        #12V Battery
        self.battery_actual_value = 0;
        self.battery_min.setText(str(self.battery_minRange)+" V")
        self.battery_max.setText(str(self.battery_maxRange)+" V")

        #motors
        self.TL_rpm_value = 0;
        self.BL_rpm_value = 0;
        self.TR_rpm_value = 0;
        self.BR_rpm_value = 0;
        self.TL_temp_value = 0;
        self.BL_temp_value = 0;
        self.TR_temp_value = 0;
        self.BR_temp_value = 0;

        #Title of the entire window
        self.setWindowTitle('Cal Poly Hyperloop')
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setFixedSize(1600, 1200)
        self.move(3520, 0)


        #Used to allow GUI to be draggable
        self.oldPos = self.pos()

        self.moreCellsButton.clicked.connect(self.on_cellButton)
        self.cellsWindow = cells_window(self)
        self.cellsWindow.close()
    def on_cellButton(self):
        self.cellsWindow.show() 

    # def mousePressEvent(self, event):
    #     self.oldPos = event.globalPos()

    # def mouseMoveEvent(self, event):
    #     delta = QPoint (event.globalPos() - self.oldPos)
    #     #print(delta)
    #     self.move(self.x() + delta.x(), self.y() + delta.y())
    #     self.oldPos = event.globalPos()


    '''GUI UPDATE FUNCTIONS'''

    def update_frontPack_label(self):
        state_text = "{0:.2f}".format(self.FP_state_value) 
        volt_text = "{0:.2f}".format(self.FP_volt_value) 
        curr_text = "{0:.2f}".format(self.FP_curr_value) 
        lowTemp_text = "{0:.2f}".format(self.FP_lowTemp_Value)
        avgTemp_text = "{0:.2f}".format(self.FP_avgTemp_Value) 
        highTemp_text = "{0:.2f}".format(self.FP_highTemp_Value) 
        minCell_text = "{0:.2f}".format(self.FP_minCell_value) 
        maxCell_text = "{0:.2f}".format(self.FP_maxCell_value)
        isolator_text = "{0:.2f}".format(self.FP_isolator_value)


        self.FP_state.setText(state_text+"%")
        self.FP_volt.setText(volt_text+" V")
        self.FP_curr.setText(curr_text+" A")
        self.FP_lowTemp.setText(lowTemp_text+" C°")
        self.FP_avgTemp.setText(avgTemp_text+" C°")
        self.FP_highTemp.setText(highTemp_text+" C°")            
        self.FP_minCell.setText(minCell_text+" V")
        self.FP_maxCell.setText(maxCell_text+" V")
        self.FP_isolater.setText(isolator_text+" V")

        if self.chargeState_minRange <= self.FP_state_value <= self.chargeState_maxRange:
            self.FP_state.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.FP_state.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

        if self.volt_minRange <= self.FP_volt_value <= self.volt_maxRange:
            self.FP_podSquare.setStyleSheet("QLabel { background-color : #00a34f;}");
            self.FP_volt.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.FP_podSquare.setStyleSheet("QLabel { background-color : #9d0b0f;}");
            self.FP_volt.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

        if self.curr_minRange <= self.FP_curr_value <= self.curr_maxRange:
            self.FP_curr.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.FP_curr.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

        if self.Temp_minRange <= self.FP_lowTemp_Value <= self.Temp_maxRange:
            self.FP_lowTemp.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.FP_lowTemp.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");
        
        if self.Temp_minRange <= self.FP_avgTemp_Value <= self.Temp_maxRange:
            self.FP_avgTemp.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.FP_avgTemp.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");
        
        if self.Temp_minRange <= self.FP_highTemp_Value <= self.Temp_maxRange:
            self.FP_highTemp.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.FP_highTemp.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");
        
        if self.minCell_minRange <= self.FP_minCell_value <= self.minCell_maxRange:
            self.FP_minCell.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.FP_minCell.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

        if self.maxCell_minRange <= self.FP_maxCell_value <= self.maxCell_maxRange:
            self.FP_maxCell.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.FP_maxCell.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

        if 4<=self.FP_isolator_value <=5:
            self.FP_isolater.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.FP_isolater.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

        self.cellsWindow.update_cells()

    def update_rearPack_label(self):
        state_text = "{0:.2f}".format(self.RP_state_value) 
        volt_text = "{0:.2f}".format(self.RP_volt_value) 
        curr_text = "{0:.2f}".format(self.RP_curr_value) 
        lowTemp_text = "{0:.2f}".format(self.RP_lowTemp_Value)
        avgTemp_text = "{0:.2f}".format(self.RP_avgTemp_Value) 
        highTemp_text = "{0:.2f}".format(self.RP_highTemp_Value)
        minCell_text = "{0:.2f}".format(self.RP_minCell_value) 
        maxCell_text = "{0:.2f}".format(self.RP_maxCell_value)
        isolator_text = "{0:.2f}".format(self.RP_isolator_value)

        self.RP_state.setText(state_text+"")
        self.RP_volt.setText(volt_text+" V")
        self.RP_curr.setText(curr_text+" A")
        self.RP_lowTemp.setText(lowTemp_text+" C°")
        self.RP_avgTemp.setText(avgTemp_text+" C°")
        self.RP_highTemp.setText(highTemp_text+" C°")         
        self.RP_minCell.setText(minCell_text+" V")
        self.RP_maxCell.setText(maxCell_text+" V")
        self.RP_isolater.setText(isolator_text+" V")

        if self.chargeState_minRange <= self.RP_state_value <= self.chargeState_maxRange:
            self.RP_state.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.RP_state.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

        if self.volt_minRange <= self.RP_volt_value <= self.volt_maxRange:
            self.RP_podSquare.setStyleSheet("QLabel { background-color : #00a34f;}");
            self.RP_volt.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.RP_podSquare.setStyleSheet("QLabel { background-color : #9d0b0f;}");
            self.RP_volt.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

        if self.curr_minRange <= self.RP_curr_value <= self.curr_maxRange:
            self.RP_curr.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.RP_curr.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

        if self.Temp_minRange <= self.RP_lowTemp_Value <= self.Temp_maxRange:
            self.RP_lowTemp.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.RP_lowTemp.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");
        
        if self.Temp_minRange <= self.RP_avgTemp_Value <= self.Temp_maxRange:
            self.RP_avgTemp.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.RP_avgTemp.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");
        
        if self.Temp_minRange <= self.RP_highTemp_Value <= self.Temp_maxRange:
            self.RP_highTemp.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.RP_highTemp.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");
        
        if self.minCell_minRange <= self.RP_minCell_value <= self.minCell_maxRange:
            self.RP_minCell.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.RP_minCell.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

        if self.maxCell_minRange <= self.RP_maxCell_value <= self.maxCell_maxRange:
            self.RP_maxCell.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.RP_maxCell.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

        if 4 <= self.RP_isolator_value<=5:
            self.RP_isolater.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.RP_isolater.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");


    def update_pneumatics_label(self):
        brakes_pressure = "{0:.2f}".format(self.brakes_pressure_value) 
        tensioner_pressure = "{0:.2f}".format(self.tensioner_pressure_value) 
        breaking_airTank = "{0:.2f}".format(self.brakes_airTank_temp_value) 
        tensioner_airtTank = "{0:.2f}".format(self.tensioner_airTank_temp_value)
        solenoid = "{0:.2f}".format(self.solenoid_temp_value)
        frontTensioner = "{0:.2f}".format(self.frontTensioner__temp_value)
        rearTensioner = "{0:.2f}".format(self.rearTensioner__temp_value)

        self.brakes_pressure.setText(brakes_pressure+" PSI")
        self.tensioner_pressure.setText(tensioner_pressure+" PSI")
        self.breaking_airTank.setText(breaking_airTank+" C°")
        self.tensioner_airTank.setText(tensioner_airtTank+" C°")
        self.solenoid.setText(solenoid+" C°")
        self.front_tensioner.setText(frontTensioner+" C°")
        self.rear_tensioner.setText(rearTensioner+" C°")

        if self.brakesPressure_minRange < self.brakes_pressure_value < self.brakesPressure_maxRange:
            self.brakes_pressure.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.brakes_pressure.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

        if self.tensionerPressure_minRange < self.tensioner_pressure_value < self.tensionerPressure_maxRange:
            self.tensioner_pressure.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.tensioner_pressure.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

        if self.breaksAirTank_minRange < self.brakes_airTank_temp_value < self.breaksAirTank_maxRange:
            self.breaking_airTank.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.breaking_airTank.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");
        
        if self.tensionerAirTank_minRange < self.tensioner_airTank_temp_value < self.tensionerAirTank_maxRange:
            self.tensioner_airTank.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.tensioner_airTank.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

        if self.solenoid_minRange < self.solenoid_temp_value < self.solenoid_maxRange:
            self.solenoid.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.solenoid.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

        if self.frontTensioner_minRange < self.frontTensioner__temp_value < self.frontTensioner_maxRange:
            self.front_tensioner.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.front_tensioner.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

        if self.rearTensioner_minRange < self.rearTensioner__temp_value < self.rearTensioner_maxRange:
            self.rear_tensioner.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.rear_tensioner.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

    def update_12Vbattery_label(self):
        voltage = "{0:.2f}".format(self.battery_actual_value) 

        self.battery_actual.setText(voltage+" V")

        if self.battery_minRange < self.battery_actual_value < self.battery_maxRange:
            self.MP_podSquare.setStyleSheet("QLabel { background-color : #00a34f;}");
            self.battery_actual.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.MP_podSquare.setStyleSheet("QLabel { background-color : #9d0b0f;}");
            self.battery_actual.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

    def update_motors_label(self):
        top_left_rpm = "{0:.2f}".format(self.TL_rpm_value) 
        top_right_rpm = "{0:.2f}".format(self.TR_rpm_value) 
        bottom_left_rpm = "{0:.2f}".format(self.BL_rpm_value) 
        bottom_right_rpm = "{0:.2f}".format(self.BR_rpm_value) 
        top_left_temp = "{0:.2f}".format(self.TL_temp_value) 
        top_right_temp = "{0:.2f}".format(self.TR_temp_value) 
        bottom_left_temp = "{0:.2f}".format(self.BL_temp_value) 
        bottom_right_temp = "{0:.2f}".format(self.BR_temp_value)

        self.TL_rpm.setText(top_left_rpm+" RPM")
        self.TR_rpm.setText(top_right_rpm+" RPM")
        self.BL_rpm.setText(bottom_left_rpm+" RPM")
        self.BR_rpm.setText(bottom_right_rpm+" RPM")
        self.TL_temp.setText(top_left_temp+" C°")
        self.TR_temp.setText(top_right_temp+" C°")
        self.BL_temp.setText(bottom_left_temp+" C°")
        self.BR_temp.setText(bottom_right_temp+" C°")

        if self.motorTemp_minRange < self.TL_temp_value < self.motorTemp_maxRange:
            self.TL_tempCircle.setStyleSheet("QLabel {background:rgba(57, 181, 74, .5); border-radius: 22;}");
        else:
            self.TL_tempCircle.setStyleSheet("QLabel {background:rgba(239, 15, 15, 0.5); border-radius: 22;}");

        if self.motorTemp_minRange < self.TR_temp_value < self.motorTemp_maxRange:
            self.TR_tempCircle.setStyleSheet("QLabel {background:rgba(57, 181, 74, .5); border-radius: 22;}");
        else:
            self.TR_tempCircle.setStyleSheet("QLabel {background:rgba(239, 15, 15, 0.5); border-radius: 22;}");

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

    RECIEVED_JSON = s.recv(6000)
    recieved = '{'+RECIEVED_JSON.decode().split('}{')[-1].strip('{')

    try:
        data = recieved
        print("************************************************************************")
        print("************************************************************************")
        print("************************************************************************")
        print("************************************************************************")
        print("************************************************************************")
        print(data)
        print("************************************************************************")
        print("************************************************************************")
        print("************************************************************************")
        print("************************************************************************")
        print("************************************************************************")
        json_parsed = json.loads(data)

        '''UPDATE DATA _SCREEN 1'''
        widget1.state = json_parsed["state"]
        widget1.acceleration = float(json_parsed["location"]["acceleration"])
        widget1.speed =  int(json_parsed["location"]["velocity"])
        widget1.distance =  int(json_parsed["location"]["position"])

        '''UPDATE DATA _SCREEN 2'''
        #FRONT PACK
        try:
            widget2.FP_state_value = float(json_parsed["1307"]["state of charge"])
        except:
            widget2.FP_state_value = -999
        try:
            widget2.FP_volt_value = float(json_parsed["1305"]["instant voltage"])
        except:
            widget2.FP_volt_value = -999
        try:
            widget2.FP_curr_value = float(json_parsed["1305"]["current"])
        except:
            widget2.FP_curr_value = -999        
        try:
            widget2.FP_lowTemp_Value = float(json_parsed["1307"]["min temp"])
        except:
            widget2.FP_lowTemp_Value = -999
        try:
            widget2.FP_avgTemp_Value = float(json_parsed["1307"]["avg temp"])
        except:
            widget2.FP_avgTemp_Value = -999
        try:
            widget2.FP_highTemp_Value = float(json_parsed["1307"]["max temp"])
        except:
            widget2.FP_highTemp_Value = -999
        try:
            widget2.FP_minCell_value = float(json_parsed["1305"]["min v"])
        except:
            widget2.FP_minCell_value = -999
        try:
            widget2.FP_maxCell_value = float(json_parsed["1305"]["max v"])
        except:
            widget2.FP_maxCell_value = -999
        try:
            widget2.FP_isolator_value = float(json_parsed["1307"]["isolater"])
        except:
            widget2.FP_isolator_value = -999

        # widget2.FP_cell1 += .1
        # widget2.FP_cell2 += .2
        # widget2.FP_cell3 += .3
        # widget2.FP_cell4 += .4
        # widget2.FP_cell5 += .5
        # widget2.FP_cell6 += .6
        # widget2.FP_cell7 += .7
        # widget2.FP_cell8 += .8

        #REAR PACK
        try:
            widget2.RP_state_value = float(json_parsed["1339"]["state of charge"])
        except:
            widget2.RP_state_value = -999
        try:
            widget2.RP_volt_value = float(json_parsed["1337"]["instant voltage"])
        except:
            widget2.RP_volt_value = -999
        try:
            widget2.RP_curr_value = float(json_parsed["1337"]["current"])
        except:
            widget2.RP_curr_value = -999
        try:
            widget2.RP_lowTemp_Value = float(json_parsed["1339"]["min temp"])
        except:
            widget2.RP_lowTemp_Value = -999
        try:
            widget2.RP_avgTemp_Value = float(json_parsed["1339"]["avg temp"])
        except:
            widget2.RP_avgTemp_Value = -999
        try:
            widget2.RP_highTemp_Value = float(json_parsed["1339"]["max temp"])
        except:
            widget2.RP_highTemp_Value = -999
        try:
            widget2.RP_minCell_value = float(json_parsed["1337"]["min v"])
        except:
            widget2.RP_minCell_value = -999
        try:
            widget2.RP_maxCell_value = float(json_parsed["1337"]["max v"])
        except:
            idget2.RP_maxCell_value = -999
        try:
            widget2.RP_isolator_value = float(json_parsed["1339"]["isolater"])
        except:
            widget2.RP_isolator_value = -999

        # widget2.RP_cell1 += .1
        # widget2.RP_cell2 += .2
        # widget2.RP_cell3 += .3
        # widget2.RP_cell4 += .4
        # widget2.RP_cell5 += .5
        # widget2.RP_cell6 += .6
        # widget2.RP_cell7 += .7
        # widget2.RP_cell8 += .8

        

        #PNEUMATICS
        try:
            widget2.brakes_pressure_value = float(json_parsed["522"]["pressure"])
        except:
            widget2.brakes_pressure_value = -999
        try:
            widget2.tensioner_pressure_value = float(json_parsed["778"]["pressure"])
        except:
            widget2.tensioner_pressure_value = -999
        try:
            widget2.brakes_airTank_temp_value = float(json_parsed["522"]["tank temp"])
        except:
            widget2.brakes_airTank_temp_value = -999
        try:
            widget2.tensioner_airTank_temp_value = float(json_parsed["778"]["tank temp"])
        except:
            widget2.tensioner_airTank_temp_value = -999
        try:
            widget2.solenoid_temp_value = float(json_parsed["778"]["solenoid temp"])
        except:
            widget2.solenoid_temp_value = -999
        try:
            widget2.frontTensioner__temp_value = float(json_parsed["778"]["front pneumatic temp"])
        except:
            widget2.frontTensioner__temp_value = -999
        try:
            widget2.rearTensioner__temp_value = float(json_parsed["779"]["back pneumatic temp"])
        except:
            widget2.rearTensioner__temp_value = -999
        
        #12V Battery
        try:
            widget2.battery_actual_value = float(json_parsed["1338"]["controls voltage"])
        except:
            widget2.battery_actual_value = -999

        #motors
        try:
            widget2.TL_rpm_value = float(json_parsed["297"]["rpm"])
        except:
            widget2.TL_rpm_value = -999
        try:
            widget2.BL_rpm_value = float(json_parsed["361"]["rpm"])
        except:
            widget2.BL_rpm_value = -999
        try:
            widget2.TR_rpm_value = float(json_parsed["281"]["rpm"])
        except:
            widget2.TR_rpm_value = -999
        try:
            widget2.BR_rpm_value = float(json_parsed["345"]["rpm"])
        except:
            widget2.BR_rpm_value = -999
        try:
            widget2.TL_temp_value = float(json_parsed["297"]["temp"])
        except:
            widget2.TL_temp_value = -999
        try:
            widget2.BL_temp_value = float(json_parsed["361"]["temp"])
        except:
            widget2.BL_temp_value = -999
        try:
            widget2.TR_temp_value = float(json_parsed["281"]["temp"])
        except:
            widget2.TR_temp_value = -999
        try:
            widget2.BR_temp_value = float(json_parsed["345"]["temp"])
        except:
            widget2.BR_temp_value = -999

        #cells
        
        try:
            widget2.cellsWindow.FP_cells[0] = float(json_parsed["1308"]["1"])
        except:
            widget2.cellsWindow.FP_cells[0] =-999
        try:
            widget2.cellsWindow.FP_cells[1] =float(json_parsed["1308"]["2"])
        except:
            widget2.cellsWindow.FP_cells[1] =-999
        try:
            widget2.cellsWindow.FP_cells[2] =float(json_parsed["1308"]["3"])
        except:
            widget2.cellsWindow.FP_cells[2] =-999
        try:
            widget2.cellsWindow.FP_cells[3] =float(json_parsed["1308"]["4"])
        except:
            widget2.cellsWindow.FP_cells[3] =-999
        try:
            widget2.cellsWindow.FP_cells[4] =float(json_parsed["1308"]["5"])
        except:
            widget2.cellsWindow.FP_cells[4] =-999
        try:
            widget2.cellsWindow.FP_cells[5] =float(json_parsed["1308"]["6"])
        except:
            widget2.cellsWindow.FP_cells[5] =-999
        try:
            widget2.cellsWindow.FP_cells[6] =float(json_parsed["1308"]["7"])
        except:
            widget2.cellsWindow.FP_cells[6] =-999
        try:
            widget2.cellsWindow.FP_cells[7] =float(json_parsed["1308"]["8"])
        except:
            widget2.cellsWindow.FP_cells[7] =-999
        try:
            widget2.cellsWindow.FP_cells[8] =float(json_parsed["1308"]["9"])
        except:
            widget2.cellsWindow.FP_cells[8] =-999
        try:
            widget2.cellsWindow.FP_cells[9] =float(json_parsed["1308"]["10"])
        except:
            widget2.cellsWindow.FP_cells[9] =-999
        try:
            widget2.cellsWindow.FP_cells[10] =float(json_parsed["1308"]["11"])
        except:
            widget2.cellsWindow.FP_cells[10] =-999
        try:
            widget2.cellsWindow.FP_cells[11] =float(json_parsed["1308"]["12"])
        except:
            widget2.cellsWindow.FP_cells[11] =-999
        try:
            widget2.cellsWindow.FP_cells[12] =float(json_parsed["1308"]["13"])
        except:
            widget2.cellsWindow.FP_cells[12] =-999
        try:
            widget2.cellsWindow.FP_cells[13] =float(json_parsed["1308"]["14"])
        except:
            widget2.cellsWindow.FP_cells[13] =-999
        try:
            widget2.cellsWindow.FP_cells[14] =float(json_parsed["1308"]["15"])
        except:
            widget2.cellsWindow.FP_cells[14] =-999
        try:
            widget2.cellsWindow.FP_cells[15] =float(json_parsed["1308"]["16"])
        except:
            widget2.cellsWindow.FP_cells[15] =-999
        try:
            widget2.cellsWindow.FP_cells[16] =float(json_parsed["1308"]["17"])
        except:
            widget2.cellsWindow.FP_cells[16] =-999
        try:
            widget2.cellsWindow.FP_cells[17] =float(json_parsed["1308"]["18"])
        except:
            widget2.cellsWindow.FP_cells[17] =-999
        try:
            widget2.cellsWindow.FP_cells[18] =float(json_parsed["1308"]["19"])
        except:
            widget2.cellsWindow.FP_cells[18] =-999
        try:
            widget2.cellsWindow.FP_cells[19] =float(json_parsed["1308"]["20"])
        except:
            widget2.cellsWindow.FP_cells[19] =-999
        
        '''SECOND PACK CELLS'''
        try:
            widget2.cellsWindow.RP_cells[0] =float(json_parsed["1340"]["1"])
        except:
            widget2.cellsWindow.RP_cells[0] = -999
        try:
            widget2.cellsWindow.RP_cells[1] =float(json_parsed["1340"]["2"])
        except:
            widget2.cellsWindow.RP_cells[1] = -999
        try:
            widget2.cellsWindow.RP_cells[2] =float(json_parsed["1340"]["3"])
        except:
            widget2.cellsWindow.RP_cells[2] = -999
        try:
            widget2.cellsWindow.RP_cells[3] =float(json_parsed["1340"]["4"])
        except:
            widget2.cellsWindow.RP_cells[3] = -999
        try:
            widget2.cellsWindow.RP_cells[4] =float(json_parsed["1340"]["5"])
        except:
            widget2.cellsWindow.RP_cells[4] = -999
        try:
            widget2.cellsWindow.RP_cells[5] =float(json_parsed["1340"]["6"])
        except:
            widget2.cellsWindow.RP_cells[5] = -999
        try:
            widget2.cellsWindow.RP_cells[6] =float(json_parsed["1340"]["7"])
        except:
            widget2.cellsWindow.RP_cells[6] = -999
        try:
            widget2.cellsWindow.RP_cells[7] =float(json_parsed["1340"]["8"])
        except:
            widget2.cellsWindow.RP_cells[7] = -999
        try:
            widget2.cellsWindow.RP_cells[8] =float(json_parsed["1340"]["9"])
        except:
            widget2.cellsWindow.RP_cells[8] = -999
        try:
            widget2.cellsWindow.RP_cells[9] =float(json_parsed["1340"]["10"])
        except:
            widget2.cellsWindow.RP_cells[9] = -999
        try:
            widget2.cellsWindow.RP_cells[10] =float(json_parsed["1340"]["11"])
        except:
            widget2.cellsWindow.RP_cells[10] = -999
        try:
            widget2.cellsWindow.RP_cells[11] =float(json_parsed["1340"]["12"])
        except:
            widget2.cellsWindow.RP_cells[11] = -999
        try:
            widget2.cellsWindow.RP_cells[12] =float(json_parsed["1340"]["13"])
        except:
            widget2.cellsWindow.RP_cells[12] = -999
        try:
            widget2.cellsWindow.RP_cells[13] =float(json_parsed["1340"]["14"])
        except:
            widget2.cellsWindow.RP_cells[13] = -999
        try:
            widget2.cellsWindow.RP_cells[14] =float(json_parsed["1340"]["15"])
        except:
            widget2.cellsWindow.RP_cells[14] = -999
        try:
            widget2.cellsWindow.RP_cells[15] =float(json_parsed["1340"]["16"])
        except:
            widget2.cellsWindow.RP_cells[15] = -999
        try:
            widget2.cellsWindow.RP_cells[16] =float(json_parsed["1340"]["17"])
        except:
            widget2.cellsWindow.RP_cells[16] = -999
        try:
            widget2.cellsWindow.RP_cells[17] =float(json_parsed["1340"]["18"])
        except:
            widget2.cellsWindow.RP_cells[17] = -999
        try:
            widget2.cellsWindow.RP_cells[18] =float(json_parsed["1340"]["19"])
        except:
            widget2.cellsWindow.RP_cells[18] = -999
        try:
            widget2.cellsWindow.RP_cells[19] =float(json_parsed["1340"]["20"])
        except:
            widget2.cellsWindow.RP_cells[19] = -999

        print("workingg!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        '''UPDATE GUI _SCREEN 1'''
        widget1.update_speedLabel()
        widget1.update_distance()
        widget1.update_accelerationLabel()
        widget1.update_stateLabel()
        widget1.update_error_label("")
        '''UPDATE GUI _SCREEN 2'''
        widget2.update_frontPack_label()
        widget2.update_rearPack_label()
        widget2.update_pneumatics_label()
        widget2.update_12Vbattery_label()
        widget2.update_motors_label()
        widget2.update_error_label("")

        if widget1.state.upper() == "LAUNCHING" or widget1.launched_yet:
            widget1.start_timer()
            widget1.launched_yet = True
        elif not widget1.launched_yet:
            widget1.clear_timer()
    except Exception as e:
        print(e)
        if len(data) < 2:
            connected = False
            widget1.update_error_label("NETWORK DISCONECTED")  
            widget2.update_error_label("NETWORK DISCONECTED")          
            s.close()
            s = socket.socket()
            while not connected:
                try:
                    widget2.update_error_label("") 
                    s.connect(('192.168.0.6', 5001))
                    connected = True
                except socket.error:
                    widget1.update_error_label("RECONECTING...")
                    widget2.update_error_label("RECONECTING...")
                    print("no connection yet")
                    time.sleep(1)
                
timer = QTimer()
timer.timeout.connect(update_labels)
timer.start(20)

sys.exit(app.exec_())


if __name__ == '__main__':
    main()