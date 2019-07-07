#### The FSM for the Raspberry Pi Control System ####
from FSMConfig import config
from FSMClasses import FSM
import time
import can
import os
import health
# import brakes
# import motors

#-------------CAN NETWORK SETUP---------------
os.system("sudo /sbin/ip link set can0 up type can bitrate 500000")
time.sleep(0.1)
bus = can.interface.Bus(channel='can0', bustype='socketcan_native')

#----------------DATA STRUCTURES-----------------
CanDataIds =  {
		281 : 'FR Motor data',
		297 : 'FL Motor data',
		313 : 'MR Motor data',
		329 : 'ML Motor data',
		345 : 'RR Motor data',
		361 : 'RL Motor data',

		537 : 'FR Brake data',
		554 : 'FL Brake data',
		569 : 'MR Brake data',
		585 : 'ML Brake data',
		601 : 'RR Brake data',
		617 : 'RL Brake data',

		793 : 'FR Tensioner data',
		809 : 'FL Tensioner data',
		825 : 'MR Tensioner data',
		841 : 'ML Tensioner data',
		857 : 'RR Tensioner data',
		873 : 'RL Tensioner data',

		1049 : 'F LIDAR data',
		1065 : 'R LIDAR data',

		1305 : 'F BMS data',
		1321 : 'M BMS data',
		1337 : 'R BMS data',

		1306 : 'F BMS arduino data',
		1322 : 'M BMS arduino data',
		1338 : 'R BMS arduino data' 
		}
CanDataVals = {
		'FR Motor Data'  : None,
		'FL Motor Data'  : None,
		'MR Motor Data'  : None,
		'ML Motor Data'  : None,
		'RR Motor Data'  : None,
		'RL Motor Data'  : None,

		'FR Brake Data' : None,
		'FL Brake Data' : None,
		'MR Brake Data' : None,
		'ML Brake Data' : None,
		'RR Brake Data' : None,
		'RL Brake Data' : None,

		'FR Tensioner data' : None,
 		'FL Tensioner data' : None,
 		'MR Tensioner data' : None,
 		'ML Tensioner data' : None,
 		'RR Tensioner data' : None,
 		'RL Tensioner data' : None,

		'F LIDAR Data' : None,
		'R LIDAR Data' : None,

		'F BMS data' : None,
		'M BMS data' : None,
		'R BMS data' : None,

		'F BMS arduino data' : None,
		'M BMS arduino data' : None,
		'R BMS arduino data' : None
		}
CanDataTimes = {
		'FR Motor Data' : None,
		'FL Motor Data' : None,
		'MR Motor Data' : None,
		'ML Motor Data' : None,
		'RR Motor Data' : None,
		'RL Motor Data' : None,

		'FR Brake Data' : None,
		'FL Brake Data' : None,
		'MR Brake Data' : None,
		'ML Brake Data' : None,
		'RR Brake Data' : None,
		'RL Brake Data' : None,

		'FR Tensioner Data' : None,
		'FL Tensioner Data' : None,
		'MR Tensioner Data' : None,
		'ML Tensioner Data' : None,
		'RR Tensioner Data' : None,
		'RL Tensioner Data' : None,		

		'F LIDAR Data' : None,
		'R LIDAR Data' : None,

		'F BMS data' : None,
		'M BMS data' : None,
		'R BMS data' : None,

		'F BMS arduino data' : None,
		'M BMS arduino data' : None,
		'R BMS arduino data' : None
		}

CanRecvIds = {
		280 : 'FR Motor Recieved',
		296 : 'FL Motor Recieved',
		312 : 'MR Motor Recieved',
		328 : 'ML Motor Recieved',
		344 : 'RR Motor Recieved',
		360 : 'RL Motor Recieved',

		536 : 'FR Brake Recieved',
		536 : 'FL Brake Recieved',
		568 : 'MR Brake Recieved',
		584 : 'ML Brake Recieved',
		600 : 'RR Brake Recieved',
		616 : 'RL Brake Recieved',

		792 : 'FR Tensioner Recieved',
		807 : 'FL Tensioner Recieved',
		824 : 'MR Tensioner Recieved',
		840 : 'ML Tensioner Recieved',
		856 : 'RR Tensioner Recieved',
		872 : 'RL Tensioner Recieved',

		1048: 'F LIDAR Recieved',
		1064: 'R LIDAR Recieved',

		1304: 'F BMS Recieved',
		1320: 'M BMS Recieved',
		1336: 'R BMS Recieved',
		}
CanRecvTimes = {
		'FR Motor Recieved' : None,
		'FL Motor Recieved' : None,
		'MR Motor Recieved' : None,
		'ML Motor Recieved' : None,
		'RR Motor Recieved' : None,
		'RL Motor Recieved' : None,

		'FR Brake Recieved' : None,
		'FL Brake Recieved' : None,
		'MR Brake Recieved' : None,
		'ML Brake Recieved' : None,
		'RR Brake Recieved' : None,
		'RL Brake Recieved' : None,

		'FR Tensioner Recieved' : None,
		'FL Tensioner Recieved' : None,
		'MR Tensioner Recieved' : None,
		'ML Tensioner Recieved' : None,
		'RR Tensioner Recieved' : None,
		'RL Tensioner Recieved' : None,

		'F LIDAR Recieved' : None,
		'R LIDAR Recieved' : None,

		'F BMS Recieved' : None,
		'M BMS Recieved' : None,
		'R BMS Recieved' : None,
		}

TelemDataVals = {
	'FR Motor Torque' : None,	
	'FL Motor Torque' : None,
	'MR Motor Torque' : None,
	'ML Motor Torque' : None,
	'RR Motor Torque' : None,
	'RL Motor Torque' : None,

	'FR Wheel RPM' : None,	
	'FL Wheel RPM' : None,
	'MR Wheel RPM' : None,
	'ML Wheel RPM' : None,
	'RR Wheel RPM' : None,
	'RL Wheel RPM' : None,

	'FR Motor Voltage' : None,	
	'FL Motor Voltage' : None,
	'MR Motor Voltage' : None,
	'ML Motor Voltage' : None,
	'RR Motor Voltage' : None,
	'RL Motor Voltage' : None,

	'FR Motor Temp' : None,
	'FL Motor Temp' : None,
	'MR Motor Temp' : None,
	'ML Motor Temp' : None,
	'RR Motor Temp' : None,
	'RL Motor Temp' : None,

	'F Battery Instant Voltage' : None,
	'M Battery Instant Voltage' : None,
	'R Battery Instant Voltage' : None,

	'F Battery State of Charge' : None,
	'M Battery State of Charge' : None,
	'R Battery State of Charge' : None,	

	'F Battery Current' : None,
	'M Battery Current' : None,
	'R Battery Current' : None,

	'F Battery Max Temp' : None,
	'M Battery Max Temp' : None,
	'R Battery Max Temp' : None,

	'F Battery Min Temp' : None,
	'M Battery Min Temp' : None,	
	'R Battery Min Temp' : None,	

	'F Battery Max Voltage' : None,
	'M Battery Max Voltage' : None,
	'R Battery Max Voltage' : None,

	'F Battery Min Voltage' : None,
	'M Battery Min Voltage' : None,
	'R Battery Min Voltage' : None,

	'F Battery Discharge Enable' : None,
	'M Battery Discharge Enable' : None,
	'R Battery Discharge Enable' : None,

	'F Battery Charge Enable' : None,
	'M Battery Charge Enable' : None,
	'R Battery Charge Enable' : None,

	'FR Tensioner Read Switch' : None,	
	'FL Tensioner Read Switch' : None,
	'MR Tensioner Read Switch' : None,
	'ML Tensioner Read Switch' : None,
	'RR Tensioner Read Switch' : None,
	'RL Tensioner Read Switch' : None,

	'FR Brake Read Switch' : None,	
	'FL Brake Read Switch' : None,
	'MR Brake Read Switch' : None,
	'ML Brake Read Switch' : None,
	'RR Brake Read Switch' : None,
	'RL Brake Read Switch' : None,

	'FR Brake Temp' : None,	
	'FL Brake Temp' : None,
	'MR Brake Temp' : None,
	'ML Brake Temp' : None,
	'RR Brake Temp' : None,
	'RL Brake Temp' : None,

	'F LIDAR Distance' : None,
	'R LIDAR Distance' : None,

	'Pod Time Since Tape' : None,
	'Pod Velocity' : None,
	'Pod Position From End' : None,
	}		

#-----------------STATE CHANGING-------------------

# Instantiate the FSM as pod & drop into Startup
pod = FSM()

isRunning = True
while isRunning
	if (TelemDataVals['FR Motor Temp'] > 70 or TelemDataVals['FL Motor Temp'] > 70 or TelemDataVals['MR Motor Temp'] > 70 or TelemDataVals['ML Motor Temp'] > 70 or TelemDataVals['RR Motor Temp'] > 70 or TelemDataVals['RL Motor Temp'] > 70 or TelemDataVals['F Battery Max Temp'] > 70 or TelemDataVals['M Battery Max Temp'] > 70 or TelemDataVals['R Battery Max Temp'] > 70 or TelemDataVals['F Battery Max Voltage'] > 68 or TelemDataVals['M Battery Max Voltage'] > 68 or TelemDataVals['R Battery Max Voltage'] > 68 or TelemDataVals['F Battery Min Voltage'] < 60 or TelemDataVals['M Battery Min Voltage'] < 60 or TelemDataVals['R Battery Min Voltage'] < 60 or ((TelemDataVals['FR Motor Torque'] > 0 or TelemDataVals['FL Motor Torque'] > 0 or TelemDataVals['ML Motor Torque'] > 0 or TelemDataVals['MR Motor Torque'] > 0 or TelemDataVals['RL Motor Torque'] > 0 or TelemDataVals['RR Motor Torque'] > 0) and (TelemDataVals['FR Brake Read Switch'] == True or TelemDataVals['FL Brake Read Switch'] == True or TelemDataVals['ML Brake Read Switch'] == True or TelemDataVals['MR Brake Read Switch'] == True or TelemDataVals['RL Brake Read Switch'] == True or TelemDataVals['RR Brake Read Switch'] == True or )) or TelemDataVals['F Battery Current'] > 250 or  TelemDataVals['M Battery Current'] > 250 or  TelemDataVals['R Battery Current'] > 250 or TelemCommand == 'Fault'): 
	#Need to add loss of comms fault, pressure faults
		pod.trigger('fault')

	if (pod.state == 'Fault' and !(TelemDataVals['FR Motor Temp'] > 70 or TelemDataVals['FL Motor Temp'] > 70 or TelemDataVals['MR Motor Temp'] > 70 or TelemDataVals['ML Motor Temp'] > 70 or TelemDataVals['RR Motor Temp'] > 70 or TelemDataVals['RL Motor Temp'] > 70 or TelemDataVals['F Battery Max Temp'] > 70 or TelemDataVals['M Battery Max Temp'] > 70 or TelemDataVals['R Battery Max Temp'] > 70 or TelemDataVals['F Battery Max Voltage'] > 68 or TelemDataVals['M Battery Max Voltage'] > 68 or TelemDataVals['R Battery Max Voltage'] > 68 or TelemDataVals['F Battery Min Voltage'] < 60 or TelemDataVals['M Battery Min Voltage'] < 60 or TelemDataVals['R Battery Min Voltage'] < 60 or ((TelemDataVals['FR Motor Torque'] > 0 or TelemDataVals['FL Motor Torque'] > 0 or TelemDataVals['ML Motor Torque'] > 0 or TelemDataVals['MR Motor Torque'] > 0 or TelemDataVals['RL Motor Torque'] > 0 or TelemDataVals['RR Motor Torque'] > 0) and (TelemDataVals['FR Brake Read Switch'] == True or TelemDataVals['FL Brake Read Switch'] == True or TelemDataVals['ML Brake Read Switch'] == True or TelemDataVals['MR Brake Read Switch'] == True or TelemDataVals['RL Brake Read Switch'] == True or TelemDataVals['RR Brake Read Switch'] == True or )) or TelemDataVals['F Battery Current'] > 250 or  TelemDataVals['M Battery Current'] > 250 or  TelemDataVals['R Battery Current'] > 250)): 
		pod.trigger('safe_to_approach')

	if (pod.state == 'SafeToApproach' and TelemCommand == 'Crawl'):
		pod.trigger('crawling')

	if (pod.state == 'ReadyToLaunch' and TelemCommand == 'Launch'):
		pod.trigger('launching')

	if (pod.state == 'Launching' and TelemDataVals['Pod Velocity'] > 105 ):
		pod.trigger('coasting')

	if (pod.state == 'Launching' and TelemDataVals['Pod Position From End'] < 1763):
		pod.trigger('braking') 

	if (pod.state == 'Coasting' and TelemDataVals['Pod Position From End'] < 1763):
		pod.trigger('braking')

	if (pod.state == 'Braking' and TelemDataVals['Pod Position From End'] < 100 and TelemDataVals['Pod Velocity'] == 0):
		pod.trigger('safe_to_approach') 

	if (pod.state == 'Braking' and TelemDataVals['Pod Position From End'] > 100 and TelemDataVals['Pod Velocity'] == 0):
		pod.trigger('crawling')

	if (pod.state == 'Crawling' and TelemDataVals['Pod Position From End'] < 100):
		pod.trigger('braking')

	if (pod.state == 'Startup' and TeleCommand == 'PrepareToLaunch')
		pod.trigger('ready_to_launch')

	if (TeleCommand == 'Startup')
		pod = FSM()

#-------------------CAN RECEPTION----------------------------

	timer1 = time.time()
	for msg in bus:
		if (msg.arbitration_id in CanDataIds):
			CanDataVals[CanDataIds[msg.arbitration_id]] = msg.data
			CanDataTimes[CanDataIds[msg.arbitration_id]] = msg.timestamp
		if (msg.arbitration_id in CanRecvIds):
			CanRecvTimes[CanRecvIds[msg.arbitration_id]] = msg.timestamp
		if (time.time() <= timer1+.1):
			break

#-----------------NETWORK RECEPTION--------------------------

#TelemCommand = NetworkRecieve() This is wishful code currently

#---------------TELEMETRY CALCULATION------------------------

#TelemDataVals = TelemCalc(CanDataVals,CanDataTimes) This is also wishful code

#---------------NETWORK TELEMETRY TRANSMISSION-----------------------

# NetworkSend(TelemDataVals) This is also wishful code currently
	   
sys.exit()