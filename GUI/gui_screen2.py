import sys
from PyQt5.QtCore import pyqtSlot, QTimer, Qt, QPoint
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.uic import loadUi
from PyQt5 import QtGui
import threading

class GUI(QMainWindow):
    def __init__(self):
        super(GUI, self).__init__()
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
        self.tensionerPressure_minRange = 50;
        self.tensionerPressure_maxRange = 150;
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
        self.FP_cell1 = 0;
        self.FP_cell2 = 0;
        self.FP_cell3 = 0;
        self.FP_cell4 = 0;
        self.FP_cell5 = 0;
        self.FP_cell6 = 0;
        self.FP_cell7 = 0;
        self.FP_cell8 = 0;
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
        self.RP_cell1 = 0;
        self.RP_cell2 = 0;
        self.RP_cell3 = 0;
        self.RP_cell4 = 0;
        self.RP_cell5 = 0;
        self.RP_cell6 = 0;
        self.RP_cell7 = 0;
        self.RP_cell8 = 0;
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
        self.move(0, 10)


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
        lowTemp_text = "{0:.2f}".format(self.FP_lowTemp_Value)
        avgTemp_text = "{0:.2f}".format(self.FP_avgTemp_Value) 
        highTemp_text = "{0:.2f}".format(self.FP_highTemp_Value) 
        minCell_text = "{0:.2f}".format(self.FP_minCell_value) 
        maxCell_text = "{0:.2f}".format(self.FP_maxCell_value)
        cell1_text = "{0:.2f}".format(self.FP_cell1)
        cell2_text = "{0:.2f}".format(self.FP_cell2)
        cell3_text = "{0:.2f}".format(self.FP_cell3)
        cell4_text = "{0:.2f}".format(self.FP_cell4)
        cell5_text = "{0:.2f}".format(self.FP_cell5)
        cell6_text = "{0:.2f}".format(self.FP_cell6)
        cell7_text = "{0:.2f}".format(self.FP_cell7)
        cell8_text = "{0:.2f}".format(self.FP_cell8)
        isolator_text = "{0:.2f}".format(self.FP_isolator_value)


        self.FP_state.setText(state_text+"%")
        self.FP_volt.setText(volt_text+" V")
        self.FP_curr.setText(curr_text+" A")
        self.FP_lowTemp.setText(lowTemp_text+" C°")
        self.FP_avgTemp.setText(avgTemp_text+" C°")
        self.FP_highTemp.setText(highTemp_text+" C°")            
        self.FP_minCell.setText(minCell_text+" V")
        self.FP_maxCell.setText(maxCell_text+" V")
        self.FP_cv1.setText(cell1_text+" V")
        self.FP_cv2.setText(cell2_text+" V")
        self.FP_cv3.setText(cell3_text+" V")
        self.FP_cv4.setText(cell4_text+" V")
        self.FP_cv5.setText(cell5_text+" V")
        self.FP_cv6.setText(cell6_text+" V")
        self.FP_cv7.setText(cell7_text+" V")
        self.FP_cv8.setText(cell8_text+" V")
        self.FP_isolater.setText(isolator_text)

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

        if self.Temp_minRange < self.FP_lowTemp_Value < self.Temp_maxRange:
            self.FP_lowTemp.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.FP_lowTemp.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");
        
        if self.Temp_minRange < self.FP_avgTemp_Value < self.Temp_maxRange:
            self.FP_avgTemp.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.FP_avgTemp.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");
        
        if self.Temp_minRange < self.FP_highTemp_Value < self.Temp_maxRange:
            self.FP_highTemp.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.FP_highTemp.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");
        
        if self.minCell_minRange < self.FP_minCell_value < self.minCell_maxRange:
            self.FP_minCell.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.FP_minCell.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

        if self.maxCell_minRange < self.FP_maxCell_value < self.maxCell_maxRange:
            self.FP_maxCell.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.FP_maxCell.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

        batteryCells = [self.FP_cell1,self.FP_cell2,self.FP_cell3,self.FP_cell4,self.FP_cell5,self.FP_cell6,self.FP_cell7,self.FP_cell8]
        cellsText = [self.FP_cv1, self.FP_cv2, self.FP_cv3, self.FP_cv4, self.FP_cv5, self.FP_cv6, self.FP_cv7, self.FP_cv8]
   
        for cell in range(len(batteryCells)):
            if self.minCell_minRange < batteryCells[cell] < self.maxCell_maxRange:
                cellsText[cell].setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
            else:
                cellsText[cell].setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

        if self.FP_isolator_value==1:
            self.FP_isolater.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.FP_isolater.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

    def update_rearPack_label(self):
        state_text = "{0:.2f}".format(self.RP_state_value) 
        volt_text = "{0:.2f}".format(self.RP_volt_value) 
        curr_text = "{0:.2f}".format(self.RP_curr_value) 
        lowTemp_text = "{0:.2f}".format(self.RP_lowTemp_Value)
        avgTemp_text = "{0:.2f}".format(self.RP_avgTemp_Value) 
        highTemp_text = "{0:.2f}".format(self.RP_highTemp_Value)
        minCell_text = "{0:.2f}".format(self.RP_minCell_value) 
        maxCell_text = "{0:.2f}".format(self.RP_maxCell_value)
        cell1_text = "{0:.2f}".format(self.RP_cell1)
        cell2_text = "{0:.2f}".format(self.RP_cell2)
        cell3_text = "{0:.2f}".format(self.RP_cell3)
        cell4_text = "{0:.2f}".format(self.RP_cell4)
        cell5_text = "{0:.2f}".format(self.RP_cell5)
        cell6_text = "{0:.2f}".format(self.RP_cell6)
        cell7_text = "{0:.2f}".format(self.RP_cell7)
        cell8_text = "{0:.2f}".format(self.RP_cell8)
        isolator_text = "{0:.2f}".format(self.RP_isolator_value)

        self.RP_state.setText(state_text+"")
        self.RP_volt.setText(volt_text+" V")
        self.RP_curr.setText(curr_text+" A")
        self.RP_lowTemp.setText(lowTemp_text+" C°")
        self.RP_avgTemp.setText(avgTemp_text+" C°")
        self.RP_highTemp.setText(highTemp_text+" C°")         
        self.RP_minCell.setText(minCell_text+" V")
        self.RP_maxCell.setText(maxCell_text+" V")
        self.RP_cv1.setText(cell1_text+" V")
        self.RP_cv2.setText(cell2_text+" V")
        self.RP_cv3.setText(cell3_text+" V")
        self.RP_cv4.setText(cell4_text+" V")
        self.RP_cv5.setText(cell5_text+" V")
        self.RP_cv6.setText(cell6_text+" V")
        self.RP_cv7.setText(cell7_text+" V")
        self.RP_cv8.setText(cell8_text+" V")
        self.RP_isolater.setText(isolator_text)

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

        if self.Temp_minRange < self.RP_lowTemp_Value < self.Temp_maxRange:
            self.RP_lowTemp.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.RP_lowTemp.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");
        
        if self.Temp_minRange < self.RP_avgTemp_Value < self.Temp_maxRange:
            self.RP_avgTemp.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.RP_avgTemp.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");
        
        if self.Temp_minRange < self.RP_highTemp_Value < self.Temp_maxRange:
            self.RP_highTemp.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.RP_highTemp.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");
        
        if self.minCell_minRange < self.RP_minCell_value < self.minCell_maxRange:
            self.RP_minCell.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.RP_minCell.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

        if self.maxCell_minRange < self.RP_maxCell_value < self.maxCell_maxRange:
            self.RP_maxCell.setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
        else:
            self.RP_maxCell.setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");

        batteryCells = [self.RP_cell1,self.RP_cell2,self.RP_cell3,self.RP_cell4,self.RP_cell5,self.RP_cell6,self.RP_cell7,self.RP_cell8]
        cellsText = [self.RP_cv1, self.RP_cv2, self.RP_cv3, self.RP_cv4, self.RP_cv5, self.RP_cv6, self.RP_cv7, self.RP_cv8]
   
        for cell in range(len(batteryCells)):
            if self.minCell_minRange < batteryCells[cell] < self.maxCell_maxRange:
                cellsText[cell].setStyleSheet("QLabel { background-color : #39b54a; border-radius: 10px; color:white;}");
            else:
                cellsText[cell].setStyleSheet("QLabel { background-color : #ef0f0f; border-radius: 10px; color:white;}");
        
        if self.RP_isolator_value==1:
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
widget = GUI()
widget.show()

def update_labels():
    '''RECIEVE ALL DATA HERE
    NOTE: currently just simulating data chagnes
    '''
    #FRONT PACK
    widget.FP_state_value += .1;
    widget.FP_volt_value += .1;
    widget.FP_curr_value += .1;
    widget.FP_lowTemp_Value +=.1
    widget.FP_avgTemp_Value +=.2
    widget.FP_highTemp_Value +=.3
    widget.FP_minCell_value += .1;
    widget.FP_maxCell_value += .1;

    widget.FP_cell1 += .1
    widget.FP_cell2 += .2
    widget.FP_cell3 += .3
    widget.FP_cell4 += .4
    widget.FP_cell5 += .5
    widget.FP_cell6 += .6
    widget.FP_cell7 += .7
    widget.FP_cell8 += .8

    widget.FP_isolator_value = 1

    #REAR PACK
    widget.RP_state_value += .1;
    widget.RP_volt_value += .1;
    widget.RP_curr_value += .1;
    widget.RP_lowTemp_Value +=.1
    widget.RP_avgTemp_Value +=.2
    widget.RP_highTemp_Value +=.3    
    widget.RP_minCell_value += .1;
    widget.RP_maxCell_value += .1;

    widget.RP_cell1 += .1
    widget.RP_cell2 += .2
    widget.RP_cell3 += .3
    widget.RP_cell4 += .4
    widget.RP_cell5 += .5
    widget.RP_cell6 += .6
    widget.RP_cell7 += .7
    widget.RP_cell8 += .8

    widget.RP_isolator_value = 1

    #PNEUMATICS
    widget.brakes_pressure_value += .1;
    widget.tensioner_pressure_value += .1;
    widget.brakes_airTank_temp_value += .1;
    widget.tensioner_airTank_temp_value += .1;
    widget.solenoid_temp_value += .1;
    widget.frontTensioner__temp_value += .2;
    widget.rearTensioner__temp_value += .3;

    #12V Battery
    widget.battery_actual_value += .1;

    #motors
    widget.TL_rpm_value += .1;
    widget.BL_rpm_value += .1;
    widget.TR_rpm_value += .1;
    widget.BR_rpm_value += .1;
    widget.TL_temp_value += .1;
    widget.BL_temp_value += .1;
    widget.TR_temp_value += .1;
    widget.BR_temp_value += .1;


    '''UPDATE GUI'''
    widget.update_frontPack_label()
    widget.update_rearPack_label()
    widget.update_pneumatics_label()
    widget.update_12Vbattery_label()
    widget.update_motors_label()
    widget.update_error_label("Error: code error "+str(widget.TL_rpm_value))

timer = QTimer()
timer.timeout.connect(update_labels)
timer.start(50)

sys.exit(app.exec_())


if __name__ == '__main__':
    main()