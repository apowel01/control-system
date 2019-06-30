#### The FSM for the Raspberry Pi Control System ####
import FSMClasses as FSM
from FSMConfig import config
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

CanDataIds =  {
		281 : 'Motor 1 data',
		297 : 'Motor 2 data',
		313 : 'Motor 3 data',
		329 : 'Motor 4 data',
		345 : 'Motor 5 data',
		361 : 'Motor 6 data',

		537 : 'Brake FR data',
		554 : 'Brake FL data',
		569 : 'Brake MR data',
		585 : 'Brake ML data',
		601 : 'Brake RR data',
		617 : 'Brake RL data',

		1049: 'LIDAR F data',
		1065: 'LIDAR R data',

		1305: 'BMS F data',
		1321: 'BMS M data',
		1337: 'BMS R data',

		1306: 'BMS arduino F data',
		1322: 'BMS arduino M data',
		1338: 'BMS arduino R data' 
		}
CanDataVals = {
		'Motor 1 Data'  : None,
		'Motor 2 Data'  : None,
		'Motor 3 Data'  : None,
		'Motor 4 Data'  : None,
		'Motor 5 Data'  : None,
		'Motor 6 Data'  : None,

		'FR Brake Data' : None,
		'FL Brake Data' : None,
		'MR Brake Data' : None,
		'ML Brake Data' : None,
		'RR Brake Data' : None,
		'RL Brake Data' : None,

		'F LIDAR Data' : None,
		'R LIDAR Data' : None,

		'BMS F data' : None,
		'BMS M data' : None,
		'BMS R data' : None,

		'BMS arduino F data' : None,
		'BMS arduino M data' : None,
		'BMS arduino R data' : None
		}
CanDataTimes = {
		'Motor 1 Data'  : None,
		'Motor 2 Data'  : None,
		'Motor 3 Data'  : None,
		'Motor 4 Data'  : None,
		'Motor 5 Data'  : None,
		'Motor 6 Data'  : None,

		'FR Brake Data' : None,
		'FL Brake Data' : None,
		'MR Brake Data' : None,
		'ML Brake Data' : None,
		'RR Brake Data' : None,
		'RL Brake Data' : None,

		'F LIDAR Data' : None,
		'R LIDAR Data' : None,

		'BMS F data' : None,
		'BMS M data' : None,
		'BMS R data' : None,

		'BMS arduino F data' : None,
		'BMS arduino M data' : None,
		'BMS arduino R data' : None
		}

CanRecvIds = {
		280 : 'Motor 1 Recieved',
		296 : 'Motor 2 Recieved',
		312 : 'Motor 3 Recieved',
		328 : 'Motor 4 Recieved',
		344 : 'Motor 5 Recieved',
		360 : 'Motor 6 Recieved',

		536 : 'Brake FR Recieved',
		536 : 'Brake FL Recieved',
		568 : 'Brake MR Recieved',
		584 : 'Brake ML Recieved',
		600 : 'Brake RR Recieved',
		616 : 'Brake RL Recieved',

		792 : 'Tensioner FR Recieved',
		807 : 'Tensioner FL Recieved',
		824 : 'Tensioner MR Recieved',
		840 : 'Tensioner ML Recieved',
		856 : 'Tensioner RR Recieved',
		872 : 'Tensioner RL Recieved',

		1048: 'LIDAR F Recieved',
		1064: 'LIDAR R Recieved',

		1304: 'BMS F Recieved',
		1320: 'BMS M Recieved',
		1336: 'BMS R Recieved',
		}
CanRecvTimes = {
		'Motor 1 Recieved' : None,
		'Motor 2 Recieved' : None,
		'Motor 3 Recieved' : None,
		'Motor 4 Recieved' : None,
		'Motor 5 Recieved' : None,
		'Motor 6 Recieved' : None,

		'Brake FR Recieved' : None,
		'Brake FL Recieved' : None,
		'Brake MR Recieved' : None,
		'Brake ML Recieved' : None,
		'Brake RR Recieved' : None,
		'Brake RL Recieved' : None,

		'Tensioner FR Recieved' : None,
		'Tensioner FL Recieved' : None,
		'Tensioner MR Recieved' : None,
		'Tensioner ML Recieved' : None,
		'Tensioner RR Recieved' : None,
		'Tensioner RL Recieved' : None,

		'LIDAR F Recieved' : None,
		'LIDAR R Recieved' : None,

		'BMS F Recieved' : None,
		'BMS M Recieved' : None,
		'BMS R Recieved' : None,
}

#------------STATE CHANGING-------------------

isRunning = True
while isRunning

#-------------OLD CODE--------------------
# let the pod coast
# def coast():
#     pass

# # power on the pod systems into start up state
# def initialize_pod():
#     # check communication with vital sensors and MCUs
#     print("TODO: Check sensor readings")
#     print("TODO: Check MCU statuses")
#     print("TODO: Initialize & create motor objects")
#     print("TODO: Initialize & create brake objects")
#     # motors.create_motors()     # create motors
#     # brakes.create_brakes()     # create brake objects
#     # TODO: initialize other peripherals
#     print("I have initalized")
#     isRunning = True
#     while isRunning:

#         if  state == FSM.states["start_up"]:
#             print("****START UP****")
#             initialize_pod() # power on sequence
#             state = FSM.states["system_diagnostic"] # always move to system diagnositc state from start up

#         # SYSTEM DIAGNOSTIC
#         elif state == FSM.states["system_diagnostic"]:
#             print("****SYSTEM DIAGNOSTIC****")
#             if health.safe_to_approach_check() == True:
#                 state = FSM.states["safe_to_approach"]
#             else: # if not safe to approach, move to fault state
#                 fault = True
#                 state = FSM.states["fault"]
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



#---------------TELEMETRY CALCULATION------------------------



#---------------NETWORK TELEMETRY TRANSMISSION-----------------------
	   
sys.exit()