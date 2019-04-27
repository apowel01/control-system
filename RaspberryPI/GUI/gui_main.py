from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QThread, pyqtSignal
from gui import Ui_MainWindow
import sys
import time
import serial
import random

motorSpeed=0
speedChanged=True

class DataThread(QThread):

    # signals to send data between threads?
    sigVoltage = pyqtSignal(int)
    sigCurrent = pyqtSignal(int)
    sigTempurature = pyqtSignal(int)
    #sigSpeed = pyqtSignal(int)
    
    voltage = 0
    current = 0
    tempurature = 0
    speed = 0

    def __init__(self):
        QThread.__init__(self)

    def run(self):
        self.running = True
        readMode = 0;
        #currentTime = time();
        
        while(self.running):
            #delta = time() - currentTime
            #currentTime = time()
            #print(delta)

            # updates GUI data
            self.updateData()

            # sends data to GUI
            self.displayData()

            # -------------------------
            # TODO: Manage data input
            # -------------------------

            #if(ser.in_waiting >0):         
                # read lines from arduino sequentialy and updates data
            #    line = ser.readline()[:-3]
            #    try:
            #        value = float(line)
            #        if(readMode == 0):
            #            self.voltage = value
            #            readMode += 1
            #        elif(readMode == 1):
            #            self.current = value
            #            readMode += 1
            #        elif(readMode == 2):
            #            self.tempurature = value
            #            readMode = 0

            #    except Exception as e:
            #        pass

                    
            time.sleep(1)

    def updateData(self):
        global motorSpeed
        global speedChanged

        if speedChanged:
            print("speed, ", motorSpeed)
            # ------------------------
            # TODO: manage output
            # ------------------------

            # ser.write((b'%d\n' % motorSpeed));
            
            speedChanged = False
        else:
            print("not sending")

    def displayData(self):
        self.sigVoltage.emit(self.voltage)
        self.sigCurrent.emit(self.current)
        self.sigTempurature.emit(self.tempurature)
        #self.sigSpeed.emit(self.speed)
        # print(self.speed)


class GuiMain(QMainWindow):
    def __init__(self):
        global ser

        # init serial connection to PI
        # ser = serial.Serial('/dev/ttyACM0', 9600)
        # ser = serial.Serial('COM14', 9600)

        # Call parent constructor
        super(GuiMain, self).__init__()

        # Use designer file we imported
        self.ui = Ui_MainWindow()
        # Setup the UI
        self.ui.setupUi(self)

        self.ui.slider.valueChanged[int].connect(self.sliderChanged)

        # Show the UI
        self.show()

        # create thread for data management and connect signals
        self.thread1 = DataThread()

        self.thread1.sigVoltage.connect(self.updateVoltage)
        self.thread1.sigCurrent.connect(self.updateCurrent)
        self.thread1.sigTempurature.connect(self.updateTempurature)
        #self.thread1.sigSpeed.connect(self.updateSpeed)
        self.thread1.start()

    def updateVoltage(self, value):
        self.ui.voltageValue.setText(str(value))

    def updateCurrent(self, value):
        self.ui.currentValue.setText(str(value))
    
    def updateTempurature(self, value):
        self.ui.tempuratureValue.setText(str(value))
    
    def sliderChanged(self, value):
        self.ui.speedValue.setText(str(value))
        global motorSpeed
        global speedChanged

        speedChanged = True
        motorSpeed = int(value)
        # send data to arduino when the slider is changed
        # ser.write((b'%d\n' % int(value)));

def RunGUI():
    # Creates Application
    app = QApplication(sys.argv)
    # Creates Window from designer
    window = GuiMain()
    # Shows the window
    window.show()
    #exit the app
    sys.exit(app.exec_())

if __name__ == "__main__":
    RunGUI()