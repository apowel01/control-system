from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QCoreApplication, QObject, QRunnable, QThread, QThreadPool, pyqtSignal
import sys
import time

class ThreadClass(QThread):
	
	sigVoltage = pyqtSignal(int)
	sigCurrent = pyqtSignal(int)
	sigTempurature = pyqtSignal(int)
	#sigSpeed = pyqtSignal(int)
	
	voltage = 0
	current = 0
	tempurature = 0
	speed = 0

	def __init__(self, parent=None):
		QThread.__init__(self, parent)

	def run(self):
		self.running = True
		#currentTime = time();
		
		while(self.running):
			#delta = time() - currentTime
			#currentTime = time()
			#print(delta)
			self.updateData()
			self.displayData()
			time.sleep(1)


	def updateData(self):
		self.speed += 1

	def displayData(self):
		self.sigVoltage.emit(self.voltage)
		self.sigCurrent.emit(self.current)
		self.sigTempurature.emit(self.tempurature)
		#self.sigSpeed.emit(self.speed)

class QthreadApp(QWidget):

	def __init__(self, parent=None):
		QWidget.__init__(self, parent)
		w = 800; h = 480

		self.setWindowTitle("Test Application")
		self.setMinimumWidth(w)
		self.setMinimumHeight(h)

		font = QFont("Times", 16, QFont.Bold)

		hlayout = QHBoxLayout()

		podStatsLayout = QVBoxLayout()
		positionLayout = QVBoxLayout()

		voltageLabel = QLabel('Voltage')
		self.voltageValue = QLabel(str(0))
		currentLabel = QLabel('Current')
		self.currentValue = QLabel(str(0))
		tempuratureLabel = QLabel('Tempurature')
		self.tempuratureValue = QLabel(str(0))

		speedLabel = QLabel('Speed')
		self.speedValue = QLabel(str(0))

		self.slider = QSlider()
		self.slider.setRange(0, 100)
		self.slider.valueChanged[int].connect(self.sliderChanged)

		voltageLabel.setFont(font)
		currentLabel.setFont(font)
		tempuratureLabel.setFont(font)
		speedLabel.setFont(font)

		podStatsLayout.addWidget(voltageLabel)
		podStatsLayout.addWidget(self.voltageValue)
		podStatsLayout.addWidget(currentLabel)
		podStatsLayout.addWidget(self.currentValue)
		podStatsLayout.addWidget(tempuratureLabel)
		podStatsLayout.addWidget(self.tempuratureValue)

		positionLayout.addWidget(speedLabel)
		positionLayout.addWidget(self.speedValue)

		hlayout.addLayout(podStatsLayout)
		hlayout.addLayout(positionLayout)
		hlayout.addWidget(self.slider)

		self.setLayout(hlayout)
		self.thread1 = ThreadClass()
		self.thread1.sigVoltage.connect(self.updateVoltage)
		self.thread1.sigCurrent.connect(self.updateCurrent)
		self.thread1.sigTempurature.connect(self.updateTempurature)
		#self.thread1.sigSpeed.connect(self.updateSpeed)
		self.thread1.start()

	def updateVoltage(self, value):
		self.voltageValue.setText(str(value))

	def updateCurrent(self, value):
		self.currentValue.setText(str(value))
	
	def updateTempurature(self, value):
		self.tempuratureValue.setText(str(value))
	
	def sliderChanged(self, value):
		self.speedValue.setText(str(value))
		


def main():

	app = QApplication(sys.argv)
	myApp = QthreadApp()
	myApp.show()
	sys.exit(app.exec_())



if __name__ == '__main__':
	main()