#!/usr/bin/env python3.7
#### The FSM for the Raspberry Pi Control System ####

# Imports
# -- So all modules have access to telemetry dictionary
import builtins
builtins.telemDict = dict() # Init telem dict
# --
import os
import time
import can
import json
import asyncio # Used for asynchronous functions
import socket # Used for sending data to SpaceX
import struct # Used for forming the data packet
from FSMClasses import FSM # Grabs the FSM object

startTime = time.time()

# Dictionary which translates our state strings to corresponding integers
stateDict = {	
	'Fault': 0,
	'SafeToApproach': 1,
	'ReadyToLaunch': 2,
	'Launching': 3,
	'Coasting': 4,
	'Braking': 5,
	'Crawling': 6,
	'Startup': 1 # Startup is the same as safe to approach (to SpaceX)
	}


motor_temp_fault = 70
max_batt_temp = 70
max_V = 68
min_V = 60
max_Amp = 250

# id_dict = {
# 	'FR Motor': 281,
# 	'FL Motor': 297,
# 	'MR Motor': 313
# }

#-------------CAN NETWORK SETUP---------------
# os.system("sudo /sbin/ip link set can0 up type can bitrate 500000")
# time.sleep(0.1)

# CAN bus object
can0 = can.interface.Bus(channel='can0', bustype='socketcan_native')
os.system("sudo ifconfig can0 txqueuelen 1000")


# New telemetry dictionary
builtins.telemDict = {
	'state': None,
	281 or 'FR Motor': {
		'name': 	'FR Motor data',
		'data': 	None,
		'time': 	None,
		'time delta' :		None,
		'rpm' : 	None,
		'volt': 	None,
		'temp': 	None,
		'throttle': None
		},
	297 or 'FL Motor': {
		'name': 'FL Motor data',
		'data': 	None,
		'time': 	None,
		'time delta' :		None,
		'rpm' : 	None,
		'volt': 	None,
		'temp': 	None,
		'throttle': None
		},
	# 313 or 'MR Motor': {
	# 	'name': 'MR Motor data',
	# 	'data': 	None,
	# 	'time': 	None,
	# 'time delta' :		None,
	# 	'rpm' : 	None,
	# 	'volt': 	None,
	# 	'temp': 	None,
	# 	'throttle': None,
	# 	'torque':   None
	# 	},
	# 329 or 'ML Motor': {
	# 	'name': 'ML Motor data',
	# 	'data': 	None,
	# 	'time': 	None,
	# 'time delta' :		None,
	# 	'rpm' : 	None,
	# 	'volt': 	None,
	# 	'temp': 	None,
	# 	'throttle': None,
	# 	'torque': None
	# 	},
	345 or 'RR Motor': {
		'name': 'RR Motor data',
		'data': 	None,
		'time': 	None,
		'time delta' :		None,
		'rpm' : 	None,
		'volt': 	None,
		'temp': 	None,
		'throttle': None
		},
	361 or 'RL Motor': {
		'name': 'RL Motor data',
		'data': 	None,
		'time': 	None,
		'time delta' :		None,
		'rpm' : 	None,
		'volt': 	None,
		'temp': 	None,
		'throttle': None
		},
	522 or 'All Brakes': {
		'name': 'All brakes',
		'data': 	None,
		'time': 	None,
		'time delta' :		None,
		'tank temp':	None,	
		'pressure': None
		},
	537 or 'FR Brake': {
		'name': 'FR Brake data',
		'data': 	None,
		'time': 	None,
		'time delta' :		None,
		'reed': 	None
		},
	553 or 'FL Brake': {
		'name': 'FL Brake data',
		'data': 	None,
		'time': 	None,
		'time delta' :		None,
		'reed': 	None
		},
	# 569 or 'MR Brake': {
	# 	'name': 'MR Brake data',
	# 	'data': 	None,
	# 	'time': 	None,
	# 'time delta' :		None,
	# 	'temp': 	None,
	# 	'reed': 	None
	# 	},
	# 585 or 'ML Brake': {
	# 	'name': 'ML Brake data',
	# 	'data': 	None,
	# 	'time': 	None,
	# 'time delta' :		None,
	# 	'temp': 	None,
	# 	'reed': 	None
	# 	},
	601 or 'RR Brake': {
		'name': 'RR Brake data',
		'data': 	None,
		'time': 	None,
		'time delta' :		None,
		'reed': 	None
		},
	617 or 'RL Brake': {
		'name': 'RL Brake data',
		'data': 	None,
		'time': 	None,
		'time delta' :		None,
		'reed': 	None
		},
	778 or 'All Tensioner 1': {
		'name': 'All tensioner 1',
		'data': 	None,
		'time': 	None,
		'time delta' :		None,
		'tank temp': None,
		'front tensioner temp': None,
		'solenoid temp': None,
		'pressure': None
		},
	779 or 'All Tensioner 2': {
		'name': 'All tensioner 1',
		'data': 	None,
		'time': 	None,
		'time delta' :		None,
		'back tensioner temp': None
		},
	793 or 'FR Tensioner': {
		'name': 'FR Tensioner data',
		'data': 	None,
		'time': 	None,
		'time delta' :		None,
		'reed': 	None
		},
	809 or 'FL Tensioner': {
		'name': 'FL Tensioner data',
		'data': 	None,
		'time': 	None,
		'time delta' :		None,
		'reed': 	None
		},
	# 825 or 'MR Tensioner': {
	# 	'name': 'MR Tensioner data',
	# 	'data': 	None,
	# 	'time': 	None,
	# 'time delta' :		None,
	# 	'reed': 	None
	# 	},
	# 841 or 'ML Tensioner': {
	# 	'name': 'ML Tensioner data',
	# 	'data': 	None,
	# 	'time': 	None,
	# 'time delta' :		None,
	# 	'reed': 	None
	# 	},
	857 or 'RR Tensioner': {
		'name': 'RR Tensioner data',
		'data': 	None,
		'time': 	None,
		'time delta' :		None,
		'reed': 	None
		},
	873 or 'RL Tensioner': {
		'name': 'RL Tensioner data',
		'data': 	None,
		'time': 	None,
		'time delta' :		None,
		'reed': 	None
		},
	1049 or 'F Lidar': {
		'name': 'F Lidar data',
		'data': 			None,
		'time': 			None,
		'time delta' :		None,
		'distance' : 		None
		},
	1065 or 'R Lidar': {
		'name': 'R Lidar data',
		'data': 			None,
		'time': 			None,
		'time delta' :		None,
		'distance' : 		None
		},
	1305 or 'F BMS': {
		'name': 'F BMS data',
		'data': 			None,
		'time': 			None,
		'time delta' :		None,
		'instant voltage':	None,
		'max v' : 			None,
		'min v' :			None,
		'current' : 		None
		},
	1307 or 'F BMS 2': {
		'name': 'F BMS 2 data',
		'data': 			None,
		'time': 			None,
		'time delta' :		None,
		'state of charge' :	None,
		'min temp' :		None,
		'max temp' :		None,
		'avg temp' :        None, #Here and below needs to be added to data translation and network packets (ID will change)
		'isolater' :        None #"Isolation ADC"
		},
	1308 or 'F BMS Cells': {
		'name': 'F BMS Cells data',
		'data': 			None,
		'time': 			None,
		'time delta' :		None,
		1 			:        None, #These are voltages
		2 			:        None,
		3 			:        None,
		4 			:        None,
		5 			:        None,
		6 			:        None,
		7 			:        None,
		8 			:        None,
		9 			:        None,
		10 			:        None,
		11 			:        None,
		12 			:        None,
		13 			:        None,
		14 			:        None,
		15 			:        None,
		16 			:        None,
		17 			:        None,
		18 			:        None,
		19 			:        None,
		20 			:        None
		},
	# 1321 or 'M BMS': {
	# 	'name': 'M BMS data',
	# 	'data': 			None,
	# 	'time': 			None,
	# 'time delta' :		None,
	# 	'max batt temp' :	None,
	# 	'max v' : 			None,
	# 	'min v' : 			None,
	# 	'current' : 		None
	# 	},
	1337 or 'R BMS': {
		'name': 'F BMS data',
		'data': 			None,
		'time': 			None,
		'time delta' :		None,
		'instant voltage':	None,
		'max v' : 			None,
		'min v' :			None,
		'current' : 		None
		},
	1339 or 'R BMS 2': {
		'name': 'F BMS 2 data',
		'data': 			None,
		'time': 			None,
		'time delta' :		None,
		'state of charge' :	None,
		'min temp' :		None,
		'max temp' :		None,
		'avg temp' :        None, #Here and below needs to be added to data translation and network packets (ID will change)
		'isolater' :        None #"Isolation ADC"
		},
	1340 or 'R BMS Cells': {
		'name': 'F BMS Cells data',
		'data': 			None,
		'time': 			None,
		'time delta' :		None,
		1 			:        None, #These are voltages
		2 			:        None,
		3 			:        None,
		4 			:        None,
		5 			:        None,
		6 			:        None,
		7 			:        None,
		8 			:        None,
		9 			:        None,
		10 			:        None,
		11 			:        None,
		12 			:        None,
		13 			:        None,
		14 			:        None,
		15 			:        None,
		16 			:        None,
		17 			:        None,
		18 			:        None,
		19 			:        None,
		20 			:        None
		},
	# 1322 or 'M BMS Arduino': {
	# 	'name': 'M BMS Arduino data',
	# 	'data': 			None,
	# 	'time': 			None,
	# 'time delta' :		None,
	# 	'health' : 			None,
	#   'discharge enable':	None,
	#   'charge enable': 	None
	# 	},
	1306 or 'F BMS Arduino': {
		'name': 'F BMS Arduino data',
		'data': 			None,
		'time': 			None,
		'time delta' :		None,
		'health' :  		None,
		'discharge enable':	None,
		'charge enable': 	None
		},
	1338 or 'R BMS Arduino': {
		'name': 'R BMS Arduino data',
		'data': 			None,
		'time': 			None,
		'time delta' :		None,
		'health' :  		None,
		'discharge enable':	None,
		'charge enable': 	None,
		'controls voltage': None
		},
	1050 or 'Right Band': {
		'name': 'Right Band Data',
		'data': 			None,
		'time': 			None,
		'time delta' :		None,
		'count': 			None
		},
	1066 or 'Left Band': {
		'name': 'Left Band Data',
		'data': 			None,
		'time': 			None,
		'time delta' :		None,
		'count': 			None
		},
	'location': {
		'position':			0,
		'velocity':			0,
		'acceleration':		0
		}
	}

#LASER SENSOR sends total number of bands

startTime = time.time()

#lists cotaining data and the time of that data
positions = [[0,0]] #2D list containing [position, time stamp]
velocities = [[0,0]] #2D list containing [velocity, time stamp]
accelerations = [[0,0]] #2D list containing [acceleration, time stamp]

#Used to error proof lidar
#Allow up to 5 errors, then completely ignore the lidar
#Errors are counted when acceleration spikes unnaturally due to lidar
lidarErrorCounter = 0

hallSensor_total = 0
lastBand_1 = 0
lastBand_2 = 0

def median(lst):
	n = len(lst)
	s = sorted(lst)
	return (sum(s[n//2-1:n//2+1])/2.0, s[n//2])[n % 2] if n else None

# async def updatePosition(FlidarReading, rpms_list, bands_list):
async def updatePosition(freq = 5):
	while True:
		#FlidarReading, rpms_list, bands_list
		global startTime

		global positions
		global velocities
		global accelerations
		
		global lidarErrorCounter
		global hallSensor_total
		global lastBand_1
		global lastBand_2
		global firstCanMessage

		timeoutcount = 0
		timeouttime = 0.5
		motortimeoutcount = 0
		motortimeouttime = 0.5
		bandtimeoutcount = 0
		bandtimeouttime = 0.5
		if telemDict['F Lidar']['time delta'] < timeouttime:
			FlidarReading = telemDict['F Lidar']['distance']
		else:
			FliderReading = 300
			timoutcount =timeoutcount +1
		if telemDict['R Lidar']['time delta'] < timeouttime:
			RlidarReading = telemDict['R Lidar']['distance']
		else:
			RliderReading = 300
		rpms_list = []
		allmotorids = [281,297,345,361]
		for i in allmotorids:
			if telemDict[i]['time delta'] < motortimeouttime:
				rpms_list.append(telemDict[i]['rpm'])
			else:
				motortimeoutcount = motortimeoutcount + 1
		if motortimeoutcout > 2:
			timeoutcount = timeoutcount +1

		allbandids = ['Right Band','Left Band']
		for i in allbandids:
			if telemDict[i]['time delta'] > bandtimeouttime:
				bandtimeoutcount = bandtimeoutcount + 1
		if bandtimeoutcout > 1:
			timeoutcount = timeoutcount +1

		if timeoutcount > 1:
			pod.trigger('fault')

		bands_list = [telemDict['Right Band']['count'],telemDict['Left Band']['count']]
		#Get the current time since start
		currentTime = time.time() - startTime
		currentTimestep = time.time()-startTime

		#TotalDistance (gets last recorded position)
		CurrentDistance = positions[-1][0]
		print("current distance, ", CurrentDistance)

		#Used to calculate distance from revolutions
		circumfrence_of_wheels = 3048#####

		#Get readings from arduinos
		#convert readings to cm
		FLidar = (1250 - FlidarReading)*100
		RLidar = RlidarReading*100
		print(currentTimestep)
		HallSensors = [rpm*circumfrence_of_wheels*currentTimestep*(1/60) for rpm in rpms_list]

		LaserSensor_1 = bands_list[0]*3048 #100ft = 3048cm
		LaserSensor_2 = bands_list[1]*3048 #100ft = 3048cm

		'''PREPARE LIDAR DATA DATA'''
		#If lidar within last 100 meters and the pod has crossed 1000 meters and less than 5 errors from lidar occured
		if FlidarReading < 125 and CurrentDistance > 100000 and lidarErrorCounter <5 and time()-telemDict['F Lidar']['time'] <0.5:
			CurrentDistance = FLidar 
		if Rlidar < 12500 and CurrentDistance <150000 and time()-telemDict['R Lidar']['time'] <0.5:
			CurrentDistance = RLidar
		else:
			'''PREPARE HALLSENSOR DATA'''
			HallSensor_median = median(HallSensors)
			HallSensors_withinRange = []
			for HallSensor in HallSensors: #Filter out hall sensors that are not within range
				if abs(HallSensor/HallSensor_median-1) <.1:
					HallSensors_withinRange.append(HallSensor)

			HallSensor_distance = 0
			for HallSensor in HallSensors_withinRange: #Take the average of hall sensors within range
				HallSensor_distance += HallSensor
			HallSensor_distance = HallSensor_distance/len(HallSensors_withinRange)

			'''PREPARE LASERSENSOR DATA''' #GET BACK TO THIS
			if LaserSensor_1 != lastBand_1 or LaserSensor_2 != lastBand_2:
				hallSensor_total = 0  #Clear hall sensor distance if we just detected a band
				if LaserSensor_1 > LaserSensor_2:
					LaserSensor_distance =  LaserSensor_1
					lastBand_1 = LaserSensor_1
				else:
					LaserSensor_distance =  LaserSensor_2
					lastBand_2 = LaserSensor_2
			else:
				hallSensor_total += HallSensor_distance #Keeps track of how long we have traveled with Hall Sensor
			CurrentDistance = LaserSensor_distance + hallSensor_total
		position = CurrentDistance

		#Insert position
		positions.append([position, currentTime])

		#calculate velocity (CM/Sec)
		velocity = float(positions[-1][0]-positions[-2][0]/currentTimestep)
		velocities.append([velocity, currentTime])


		#calculate acceleration
		acceleration = float(velocity/currentTimestep)
		accelerations.append([acceleration, currentTime])

		#Check if an error occured with the lidar
		#Allow up to 5 errors
		if FlidarReading < 10000 and CurrentDistance < 100000 and lidarErrorCounter < 5:
			lidarErrorCounter += 1
		if len(positions) > 5:
			del positions[0]
			del velocities[0]
			del accelerations[0]
		#Returns current data
		#history of data can be accessed via the global lists (positions, velocities, accelerations)
		telemDict['location']['position'] = position
		telemDict['location']['velocity'] = velocity
		telemDict['location']['accleration'] = acceleration

		await asyncio.sleep(1/freq)

async def updateTelemDict(freq = 5):

	while True:
		# try:
			# timer = time.time()
			motor_id = [281,297,345,361]
			for i in motor_id:		
				if telemDict[i]['data'] != None:
					telemDict[i]['rpm'] = (telemDict[i]['data'][1] << 8) + telemDict[i]['data'][2]
					telemDict[i]['volt'] = (telemDict[i]['data'][3] << 8) + telemDict[i]['data'][4]
					telemDict[i]['temp'] = (telemDict[i]['data'][5] << 8) + telemDict[i]['data'][6]
					telemDict[i]['throttle'] = telemDict[i]['data'][7]
					
			brake_id = [537, 553, 601, 617]
			for i in brake_id:
				if telemDict[i]['data'] != None:
					telemDict[i]['reed'] = telemDict[i]['data'][7]

			tension_id = [793, 809, 857, 873]
			for i in tension_id:
				if telemDict[i]['data'] != None:
					telemDict[i]['reed'] = telemDict[i]['data'][7]
			
			pressure_id = [522, 778]
			for i in pressure_id:
				if telemDict[i]['data'] != None:
					telemDict[i]['pressure'] = (telemDict[i]['data'][6] << 8) + telemDict[i]['data'][7]

			all_brake_id = [522]
			for i in all_brake_id:
				if telemDict[i]['data'] != None:
					telemDict[i]['tank temp'] = (telemDict[i]['data'][4] << 8) + telemDict[i]['data'][5] 

			all_tensioner_id1 = [778]
			for i in all_tensioner_id1:
				if telemDict[i]['data'] != None:
					telemDict[i]['tank temp'] = (telemDict[i]['data'][4] << 8) + telemDict[i]['data'][5] 
					telemDict[i]['front tensioner temp'] = (telemDict[i]['data'][2] << 8) + telemDict[i]['data'][3] 
					telemDict[i]['solenoid temp'] = (telemDict[i]['data'][0] << 8) + telemDict[i]['data'][1] 

			all_tensioner_id2 = [779]
			for i in all_tensioner_id2:
				if telemDict[i]['data'] != None:
					telemDict[i]['back tensioner temp'] = (telemDict[i]['data'][6] << 8) + telemDict[i]['data'][7] 

			BMS_id1 = [1305,1337]
			for i in BMS_id1:
				if telemDict[i]['data'] != None:
					telemDict[i]['current'] = ((telemDict[i]['data'][0] << 8) + telemDict[i]['data'][1])*.1 #amps
					telemDict[i]['instant voltage'] = ((telemDict[i]['data'][2] << 8) + telemDict[i]['data'][3])*.1 #volts
					telemDict[i]['min v'] = ((telemDict[i]['data'][4] << 8) + telemDict[i]['data'][5])*.0001 #volts		 
					telemDict[i]['max v'] = ((telemDict[i]['data'][6] << 8) + telemDict[i]['data'][7])*.0001 #volts

			BMS_id2 = [1307,1339]
			for i in BMS_id2:
				if telemDict[i]['data'] != None:
					telemDict[i]['isolater'] = ((telemDict[i]['data'][0] << 8) + telemDict[i]['data'][1])*.001 #volts
					telemDict[i]['state of charge'] = telemDict[i]['data'][2]*.5 #percent
					telemDict[i]['max temp'] = telemDict[i]['data'][4] #deg C 
					telemDict[i]['min temp'] = telemDict[i]['data'][3] #deg C
					telemDict[i]['avg temp'] = telemDict[i]['data'][5] #deg C


			BMS_id3 = [1308,1340]
			for i in BMS_id3:
				if telemDict[i]['data'] != None:
					telemDict[i][int(telemDict[i]['data'][0]+1)] = ((telemDict[i]['data'][1] << 8) + telemDict[i]['data'][2])*.0001

			BMS_arduino_id = [1306,1338]
			for i in BMS_arduino_id:
				if telemDict[i]['data'] != None:
					telemDict[i]['discharge enable'] = telemDict[i]['data'][7]
					telemDict[i]['charge enable'] = telemDict[i]['data'][6] 
			
			Control_batt_id = [1338]
			for i in Control_batt_id:
				if telemDict[i]['data'] != None:		
					telemDict[i]['controls voltage'] = (telemDict[i]['data'][4] << 8) + telemDict[i]['data'][5]

			if (telemDict[1049]['data'] != None) and (telemDict[1065]['data'] != None) and (telemDict[1050]['data'] != None) and (telemDict[1066]['data'] != None):
				telemDict[1049]['distance'] = (telemDict[1049]['data'][6] << 8) + telemDict[1049]['data'][7]
				telemDict[1065]['distance'] = (telemDict[1065]['data'][6] << 8) + telemDict[1065]['data'][7]

				telemDict[1050]['count'] = (telemDict[1050]['data'][6] << 8) + telemDict[1050]['data'][7]
				telemDict[1066]['count'] = (telemDict[1066]['data'][6] << 8) + telemDict[1066]['data'][7]
			# print("****************************")
			# print(time.time() - timer)
			# print("****************************")
		# except Exception as e:
		# 	print("NOOOOOOOOOOOOOOOOOOOOOOOOOO")
		# 	pass
			
			await asyncio.sleep(1/freq)
	
# Command server
async def cmd_server(host, port):
	server = await asyncio.start_server(processNetCmds, host, port)
	await server.serve_forever()

# Telemetry server
async def tlm_server(host, port):
	server = await asyncio.start_server(broadcastTlm, host, port)
	await server.serve_forever()

# Process network commands
async def processNetCmds(reader, writer):

	# List of possible commands
	cmds = {
		'state': {'set': '', 'current': ''},
		'tlmset': None,
		'cancel': None,
		'abort': None,
		'fault': None,
		'stop': None
		}

	while True:
		data = await reader.read(1024) # Max number of bytes to read
		if not data: # If no commands, stop
			break

		try:
			# Try decoding data, otherwise ignore it
			cmd = data.decode('utf8').rstrip().lower().split(" ")
		except Exception as e:
			print(f"Caught exception processing network commands: {e}")
			continue

		output = '' # Init the output

		if cmd[0] == '' or cmd[0] == 'help':
			# Provide a list of possible commands
			output = f"Possible commands:  {', '.join(list(cmds.keys()))}"
		elif cmd[0] in cmds:
			if cmd[0] == 'state':
				# State-related commands
				if len(cmd) == 1:
					# Just reply with the current state
					output = f"Current state: {pod.state}"
				elif cmd[1] == 'set':
					# Set new state
					try:
						pod.trigger(cmd[2])
						output = f"Current state: {pod.state}"
					except Exception as e:
						output = f"Setting state failed: {e}"
				elif cmd[1] == 'current':
					output = f"Current state: {pod.state}"
			elif cmd[0] == 'tlmset':
				if len(cmd) == 4:
					try:
						telemDict[cmd[1]][cmd[2]] = int(cmd[3])
					except Exception as e:
						raise
			# Assume abort message
			else:
				pod.trigger('fault')
				output = f"Current state: {pod.state}"
		else:
			output = f"Invalid command: {' '.join(cmd)}"

		output = output + "\n" # Add a newline character to output for conveinience
		writer.write(output.encode('utf8'))

	writer.close()

# Broascast telemetry for telemetry server
async def broadcastTlm(reader, writer, freq = 5):
	# Init telemetry dictionary
	global telemDict
	print("Broadcasting telemetry")

	# Primary process loop
	while True:
		if writer.is_closing():
			# Watch for the client to close
			break
		
		telemDict['state'] = str(pod.state)
		# if str(pod.state) == 'Launching' or str(pod.state) == 'Coasting' or str(pod.state) == 'Braking':
		# 	telemDict['distance'] = telemDict['distance'] + 1 # Sample data

		 # Serialize dictionary as xjson (ignoring unserializable data)
		output = json.dumps(telemDict, default=lambda o: '')
		writer.write(output.encode('utf8'))

		await asyncio.sleep(1/freq) # Wait until sending telem update

	writer.close()

async def printing(freq = .1):
	global telemDict
	while True:
		print("Printing")
		print(telemDict[281]['rpm'])
		await asyncio.sleep(1/freq)

# Process CAN-based telemetry
# Input: Processing frequency [Hz]
async def processTelem(freq = 5, can_read_freq = 10):
	global telemDict # Bring in telemetry dictionary

	# while True:
	# 	# print("Trying to read can?")
	# 	timer1 = time.time()
	# 	for msg in can0:
	# 		# print("  Arbitration id")
	# 		# print(msg.arbitration_id)
	# 		# print("  Data")
	# 		# print(msg.data)
	# 		# print("  Timestamp")
	# 		# print(msg.timestamp)
	# 		# print(telemDict.keys)
	# 		try:
	# 			telemDict[msg.arbitration_id]['data'] = msg.data
	# 			telemDict[msg.arbitration_id]['time'] = msg.timestamp				
	# 		except Exception as e:
	# 			print(f"Caught exception: {e}")
	# 			continue
	# 		print(timer1)
	# 		if (time.time() >= timer1 + (1/can_read_freq)):
	# 			print("HIIII")
	# 			break

	# 	#await asyncio.sleep(1/freq)
	# 	# print("**Flag**")

	# 		# print("**MESSAGE**")
	# 		# print(telemDict[1306]['health'])
	# 		# print("**WORKS**")
			
	# 	await asyncio.sleep(1/freq)

	reader = can.AsyncBufferedReader()
	
	listeners = [reader]

	loop = asyncio.get_event_loop()
	notifier = can.Notifier(can0, listeners, loop=loop)
	# can0.flush_tx_buffer()
	print("Starting processTelem loop")
	while True:
		for _ in range(10):
			# Wait for next message from AsyncBufferedReader
			msg = await reader.get_message()
			# print(f"Processing data: {msg.data}")
			# print(f"Timestamp: {msg.timestamp}")
			# Delay response
			# await asyncio.sleep(0.05)
			try:
				telemDict[msg.arbitration_id]['data'] = msg.data
				telemDict[msg.arbitration_id]['time'] = msg.timestamp
				if telemDict[msg.arbitration_id]['time'] != None:
					telemDict[msg.arbitration_id]['time delta'] = msg.timestamp - telemDict[msg.arbitration_id]['time']

			except Exception as e:
				print(f"Caught exception processing telemetry: {e}")
				continue
		# Wait for last message to arrive
		await reader.get_message()
		await asyncio.sleep(1/freq)

		# Clean-up

async def CAN_out(freq = 5):
	global stateDict # Grab the state dictionary # Grab pod object
	
	while True:
		if (stateDict[str(pod.state)] == 3):
			message = can.Message(arbitration_id=257, data=[0, 0, 0, 0, 0, 0, 0, 0], extended_id=False)
			can0.send(message)
		elif (stateDict[str(pod.state)] == 5) or (stateDict[str(pod.state)] == 0) or (stateDict[str(pod.state)] == 1) or (stateDict[str(pod.state)] == 2) or (stateDict[str(pod.state)] == 4 or (stateDict[str(pod.state)] == 1)):
			message = can.Message(arbitration_id=256, data=[0, 0, 0, 0, 0, 0, 0, 0], extended_id=False)
			can0.send(message)
		elif (stateDict[str(pod.state)] == 6):
			print("***Crawling***")
			message = can.Message(arbitration_id=258, data=[0, 0, 0, 0, 0, 0, 0, 10], extended_id=False)
			can0.send(message)

		await asyncio.sleep(1/freq)		

# Coroutine for sending telemetry to SpaceX
# Input: Transmit frequency [Hz]
async def spacex_tlm(freq = 50):
	global stateDict # Grab the state dictionary # Grab pod object
	global telemDict

	server_ip = "192.168.0.7" # SpaceX telemetry machine
	server_port = 3000

	team_id = 4
	# Instantiate a socket object of family AF_INET and type DOCK_DGRAM
	spacexTlmSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	# Send data at rate specified by freq
	while True:
		position = 1000000	#placeholder
		velocity = 9001		#placeholder
		acceleration = 981	#placeholder
		status = stateDict[str(pod.state)]

		# Pack the string according to format BB7iI

		# Packet layout (from SpaceX)
		# team_id			 	uint8  	Identifier for the team, assigned by the
		#								organization. Required.
		# status			  	uint8  	Pod status, indicating the current state the pod
		#								is in. Required.
		# acceleration			int32  	Acceleration in centimeters per second squared.
		#								Required.
		# position				int32  	Position in centimeters. Required.
		# velocity				int32  	Velocity in centimeters per second. Required.
		# battery_voltage	 	int32  	Battery voltage in millivolts. Optional
		# battery_current	 	int32  	Battery current in milliamps. Optional
		# battery_temperature 	int32  	Battery temperature in tenths of a degree
		#								Celsius. Optional
		# pod_temperature	 	int32  	Pod temperature in tenths of a degree Celsius.
		#								optional
		# stripe_count			uint32 	Count of optical navigation stripes detected in
		#								the tube. Optional
		packet = struct.pack(">BB7iI", team_id, status, int(telemDict['location']['acceleration']), int(telemDict['location']['position']), int(telemDict['location']['velocity']), 0, 0, 0, 0, 0)
		spacexTlmSocket.sendto(packet, (server_ip, server_port))
		#-------NEW PACKETS--------
		# packet = struct.pack(">BB7iI", team_id, status, int(accelerations[-1][0]), int(positions[-1][0]), int(velocities[-1][0]), 0, 0, 0, 0, int(position) // 3048)
		# spacexTlmSocket.sendto(packet, (server_ip, server_port))
		# packet = struct.pack(">BB7iI", team_id, status, int(telemDict['FR Motor']['rpm']), int(telemDict['FL Motor']['rpm']), int(telemDict['BR Motor']['rpm']), int(telemDict['BL Motor']['rpm']), int(telemDict['FR Motor']['temp']), int(telemDict['FL Motor']['temp']), int(position) // 3048)
		# spacexTlmSocket.sendto(packet, (server_ip, server_port))
		# packet = struct.pack(">BB7iI", team_id, status, int(telemDict['BR Motor']['temp']), int(telemDict['BL Motor']['temp']), int(telemDict[1305]['state of charge']), int(telemDict[1305]['instant voltage']), int(telemDict[1305]['current']), int(telemDict[1305]['min temp']), int(position) // 3048)
		# spacexTlmSocket.sendto(packet, (server_ip, server_port))
		# packet = struct.pack(">BB7iI", team_id, status, int(telemDict[1305]['avg temp']), int(telemDict[1305]['max temp']), int(telemDict[1305]['isolater']), int(telemDict[1305]['min v']), int(telemDict[1305]['max v']), int(telemDict[1305]['cell 1 v']), int(position) // 3048)
		# spacexTlmSocket.sendto(packet, (server_ip, server_port))
		# packet = struct.pack(">BB7iI", team_id, status, int(telemDict[1305]['cell 2 v']), int(telemDict[1305]['cell 3 v']), int(telemDict[1305]['cell 4 v']), int(telemDict[1305]['cell 5 v']), int(telemDict[1305]['cell 6 v']), int(telemDict[1305]['cell 7 v']), int(position) // 3048)
		# spacexTlmSocket.sendto(packet, (server_ip, server_port))
		# packet = struct.pack(">BB7iI", team_id, status, int(telemDict[1305]['cell 8 v']), int(telemDict['R BMS']['state of charge']), int(telemDict['R BMS']['instant voltage']), int(telemDict['R BMS']['current']), int(telemDict['R BMS']['min temp']), int(telemDict['R BMS']['avg temp']), int(position) // 3048)
		# spacexTlmSocket.sendto(packet, (server_ip, server_port))
		# packet = struct.pack(">BB7iI", team_id, status, int(telemDict['R BMS']['max temp']), int(telemDict['R BMS']['isolater']), int(telemDict['R BMS']['min v']), int(telemDict['R BMS']['max v']), int(telemDict['R BMS']['cell 1 v']), int(telemDict['R BMS']['cell 2 v']), int(position) // 3048)
		# spacexTlmSocket.sendto(packet, (server_ip, server_port))
		# packet = struct.pack(">BB7iI", team_id, status, int(telemDict['R BMS']['cell 3 v']), int(telemDict['cell 4 v']['isolater']), int(telemDict['R BMS']['cell 5 v']), int(telemDict['R BMS']['cell 6 v']), int(telemDict['R BMS']['cell 7 v']), int(telemDict['R BMS']['cell 8 v']), int(position) // 3048)
		# spacexTlmSocket.sendto(packet, (server_ip, server_port))
		# packet = struct.pack(">BB7iI", team_id, status, int(telemDict['R BMS']['cell 3 v']), int(telemDict['cell 4 v']['isolater']), int(telemDict['R BMS']['cell 5 v']), int(telemDict['R BMS']['cell 6 v']), int(telemDict['R BMS']['cell 7 v']), int(telemDict['R BMS']['cell 8 v']), int(position) // 3048)
		# spacexTlmSocket.sendto(packet, (server_ip, server_port))
		# packet = struct.pack(">BB7iI", team_id, status, int(telemDict['All Brakes']['pressure']), int(telemDict['All Tensioner 1']['pressure']), int(telemDict['All Brakes']['tank temp']), int(telemDict['All Tensioner 1']['tank temp']), int(telemDict['All Tensioner 1']['solenoid temp']), int(telemDict['All Tensioner 1']['front tensioner temp']), int(position) // 3048)
		# spacexTlmSocket.sendto(packet, (server_ip, server_port))
		# packet = struct.pack(">BB7iI", team_id, status, int(telemDict['All Tensioner 2']['back tensioner temp']), 0, 0, 0, 0, 0, int(position) // 3048)
		# spacexTlmSocket.sendto(packet, (server_ip, server_port))
		#-------------------NEED TO RESTRUCTURE PACKETS
		
		# Sleep for 1/freq secs before sending another packet
		await asyncio.sleep(1/freq)

# Instantiate the FSM as pod & drop into Startup
async def init_pod():
	builtins.pod = FSM()

async def main():
	IP = "192.168.0.6" # Pi's IP address

	print(f"Host name: {socket.gethostname()}")
	print(f"IP address: {IP}")

	# Gather asynchronous coroutines
	await asyncio.gather(
		init_pod(),
		cmd_server(IP, 5000),
		tlm_server(IP, 5001),
		spacex_tlm(),
		updateTelemDict(),
		processTelem(),
		# CAN_out(),		   
		# printing(),
		# broadcastTlm(),
		# processNetCmds()
	)

# Run controls loop
asyncio.run(main())
