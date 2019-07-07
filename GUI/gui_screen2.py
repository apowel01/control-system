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
    widget.FP_minCell_value += .1;
    widget.FP_maxCell_value += .1;
    widget.FP_t1_value += .1;
    widget.FP_t2_value += .1;
    widget.FP_t3_value += .1;
    widget.FP_t4_value += .1;
    widget.FP_t5_value += .1;
    widget.FP_t6_value += .1;
    widget.FP_t7_value += .1;
    widget.FP_t8_value += .1;

    #FRONT PACK
    widget.MP_state_value += .1;
    widget.MP_volt_value += .1;
    widget.MP_curr_value += .1;
    widget.MP_minCell_value += .1;
    widget.MP_maxCell_value += .1;
    widget.MP_t1_value += .1;
    widget.MP_t2_value += .1;
    widget.MP_t3_value += .1;
    widget.MP_t4_value += .1;
    widget.MP_t5_value += .1;
    widget.MP_t6_value += .1;
    widget.MP_t7_value += .1;
    widget.MP_t8_value += .1;

    #FRONT PACK
    widget.RP_state_value += .1;
    widget.RP_volt_value += .1;
    widget.RP_curr_value += .1;
    widget.RP_minCell_value += .1;
    widget.RP_maxCell_value += .1;
    widget.RP_t1_value += .1;
    widget.RP_t2_value += .1;
    widget.RP_t3_value += .1;
    widget.RP_t4_value += .1;
    widget.RP_t5_value += .1;
    widget.RP_t6_value += .1;
    widget.RP_t7_value += .1;
    widget.RP_t8_value += .1;

    #PNEUMATICS
    widget.brakes_pressure_value += .1;
    widget.tensioner_pressure_value += .1;
    widget.brakes_temp_value += .1;    

    #12V Battery
    widget.battery_actual_value += .1;

    #motors
    widget.TL_rpm_value += .1;
    widget.ML_rpm_value += .1;
    widget.BL_rpm_value += .1;
    widget.TR_rpm_value += .1;
    widget.MR_rpm_value += .1;
    widget.BR_rpm_value += .1;
    widget.TL_temp_value += .1;
    widget.ML_temp_value += .1;
    widget.BL_temp_value += .1;
    widget.TR_temp_value += .1;
    widget.MR_temp_value += .1;
    widget.BR_temp_value += .1;


    '''UPDATE GUI'''
    widget.update_frontPack_label()
    widget.update_middlePack_label()
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