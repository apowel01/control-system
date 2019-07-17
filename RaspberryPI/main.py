#!/usr/bin/env python3.7
#### The FSM for the Raspberry Pi Control System ####

# Imports
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

telemetry = {
	'position': 0,
	'velocity': 0,
	'acceleration': 0
}


motor_temp_fault = 70
max_batt_temp = 70
max_V = 68
min_V = 60
max_Amp = 250

id_dict = {
	'FR Motor': 281,
	'FL Motor': 297,
	'MR Motor': 313
}

#-------------CAN NETWORK SETUP---------------
# os.system("sudo /sbin/ip link set can0 up type can bitrate 500000")
# time.sleep(0.1)

# CAN bus object
can0 = can.interface.Bus(channel='can0', bustype='socketcan_native')
os.system("sudo ifconfig can0 txqueuelen 1000")


# New telemetry dictionary
telemDict = {
	281 or 'FR Motor': {
		'name': 	'FR Motor data',
		'data': 	None,
		'time': 	None,
		'rpm' : 	None,
		'volt': 	None,
		'temp': 	None,
		'throttle': None,
		'torque':   None
		},
	297 or 'FL Motor': {
		'name': 'FL Motor data',
		'data': 	None,
		'time': 	None,
		'rpm' : 	None,
		'volt': 	None,
		'temp': 	None,
		'throttle': None,
		'torque':   None
		},
	# 313 or 'MR Motor': {
	# 	'name': 'MR Motor data',
	# 	'data': 	None,
	# 	'time': 	None,
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
		'rpm' : 	None,
		'volt': 	None,
		'temp': 	None,
		'throttle': None,
		'torque':   None
		},
	361 or 'RL Motor': {
		'name': 'RL Motor data',
		'data': 	None,
		'time': 	None,
		'rpm' : 	None,
		'volt': 	None,
		'temp': 	None,
		'throttle': None,
		'torque':   None
		},
	522 or 'All Brakes': {
		'name': 'All brakes',
		'data': 	None,
		'time': 	None,
		'tank temp':	None,	
		'pressure': None
		},
	537 or 'FR Brake': {
		'name': 'FR Brake data',
		'data': 	None,
		'time': 	None,
		'reed': 	None
		},
	554 or 'FL Brake': {
		'name': 'FL Brake data',
		'data': 	None,
		'time': 	None,
		'reed': 	None
		},
	# 569 or 'MR Brake': {
	# 	'name': 'MR Brake data',
	# 	'data': 	None,
	# 	'time': 	None,
	# 	'temp': 	None,
	# 	'reed': 	None
	# 	},
	# 585 or 'ML Brake': {
	# 	'name': 'ML Brake data',
	# 	'data': 	None,
	# 	'time': 	None,
	# 	'temp': 	None,
	# 	'reed': 	None
	# 	},
	601 or 'RR Brake': {
		'name': 'RR Brake data',
		'data': 	None,
		'time': 	None,
		'reed': 	None
		},
	617 or 'RL Brake': {
		'name': 'RL Brake data',
		'data': 	None,
		'time': 	None,
		'reed': 	None
		},
	778 or 'All Tensioner 1': {
		'name': 'All tensioner 1',
		'data': 	None,
		'time': 	None,
		'tank temp': None,
		'front pneumatic temp': None,
		'solenoid temp': None,
		'pressure': None
		},
	779 or 'All Tensioner 2' {
		'name': 'All tensioner 1',
		'data': 	None,
		'time': 	None,
		'back pneumatic temp': None
	}
	793 or 'FR Tensioner': {
		'name': 'FR Tensioner data',
		'data': 	None,
		'time': 	None,
		'reed': 	None
		},
	809 or 'FL Tensioner': {
		'name': 'FL Tensioner data',
		'data': 	None,
		'time': 	None,
		'reed': 	None
		},
	# 825 or 'MR Tensioner': {
	# 	'name': 'MR Tensioner data',
	# 	'data': 	None,
	# 	'time': 	None,
	# 	'reed': 	None
	# 	},
	# 841 or 'ML Tensioner': {
	# 	'name': 'ML Tensioner data',
	# 	'data': 	None,
	# 	'time': 	None,
	# 	'reed': 	None
	# 	},
	857 or 'RR Tensioner': {
		'name': 'RR Tensioner data',
		'data': 	None,
		'time': 	None,
		'reed': 	None
		},
	873 or 'RL Tensioner': {
		'name': 'RL Tensioner data',
		'data': 	None,
		'time': 	None,
		'reed': 	None
		},
	1049 or 'F Lidar': {
		'name': 'F Lidar data',
		'data': 			None,
		'time': 			None,
		'distance' : 		None
		},
	1065 or 'R Lidar': {
		'name': 'R Lidar data',
		'data': 			None,
		'time': 			None,
		'distance' : 		None
		},
	249 or 'R Band': {
		'name': 'R Band data',
		'data': 			None,
		'time': 			None,
		'count' :				0
		},
	265 or 'L Band':{
		'name': 'L Band data',
		'data': 			None,
		'time': 			None,
		'count' : 				0
		},
	1305 or 'F BMS': {
		'name': 'F BMS data',
		'data': 			None,
		'time': 			None,
		'max batt temp' :   None,
		'max v' : 			None,
		'min v' :			None,
		'current' : 		None
		},
	# 1321 or 'M BMS': {
	# 	'name': 'M BMS data',
	# 	'data': 			None,
	# 	'time': 			None,
	# 	'max batt temp' :	None,
	# 	'max v' : 			None,
	# 	'min v' : 			None,
	# 	'current' : 		None
	# 	},
	1337 or 'R BMS': {
		'name': 'R BMS data',
		'data': 			None,
		'time': 			None,
		'max batt temp' :	None,
		'max v' : 			None,
		'min v' : 			None,
		'current' : 		None
		},
	1306 or 'F BMS Arduino': {
		'name': 'F BMS Arduino data',
		'data': 			None,
		'time': 			None,
		'health' :  		None,
		'discharge enable':	None,
		'charge enable': 	None
		},
	# 1322 or 'M BMS Arduino': {
	# 	'name': 'M BMS Arduino data',
	# 	'data': 			None,
	# 	'time': 			None,
	# 	'health' : 			None,
	#   'discharge enable':	None,
	#   'charge enable': 	None
	# 	},
	1338 or 'R BMS Arduino': {
		'name': 'R BMS Arduino data',
		'data': 			None,
		'time': 			None,
		'health' :  		None,
		'discharge enable':	None,
		'charge enable': 	None
		},
	1050: {
		'name': 'Left Band',
		'data': None,
		'time': None,
		'count': None
		},
	1051: {
		'name': 'Left Band',
		'data': None,
		'time': None,
		'count': None
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

# async def updatePosition(lidarReading, rpms_list, bands_list):
def updatePosition(lidarReading, rpms_list, bands_list):
    global startTime

    global positions
    global velocities
    global accelerations
    
    global lidarErrorCounter
    global hallSensor_total
    global lastBand_1
    global lastBand_2
    global firstCanMessage

    #Get the current time since start
    currentTime = time.time() - startTime
    currentTimestep = time.time()-positions[-1][1]-startTime
    # currentTimestep = time.time()-currentTime 

    #TotalDistance (gets last recorded position)
    CurrentDistance = positions[-1][0]
    print("current distance, ", CurrentDistance)

    #Used to calculate distance from revolutions
    circumfrence_of_wheels = 3048#####

    #Get readings from arduinos
    #convert readings to cm
    Lidar = (1250 - lidarReading)*100
    print(currentTimestep)
    HallSensors = [rpm*circumfrence_of_wheels*currentTimestep*(1/60) for rpm in rpms_list]

    LaserSensor_1 = bands_list[0]*3048 #100ft = 3048cm
    LaserSensor_2 = bands_list[1]*3048 #100ft = 3048cm

    '''PREPARE LIDAR DATA DATA'''
    #If lidar within last 100 meters and the pod has crossed 1000 meters and less than 5 errors from lidar occured
    if lidarReading < 10000 and CurrentDistance > 100000 and lidarErrorCounter <5:
        CurrentDistance = Lidar 
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
    if lidarReading < 10000 and CurrentDistance < 100000 and lidarErrorCounter < 5:
        lidarErrorCounter += 1
    if len(positions) > 5
    	del positions[0]
    	del velocities[0]
    	del accelerations[0]
    #Returns current data
    #history of data can be accessed via the global lists (positions, velocities, accelerations)
    return [position, velocity, acceleration]


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
					
			brake_id = [537, 554, 601, 617]
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
			for i in pressure_id1:
				if telemDict[i]['data'] != None:
					telemDict[i]['tank temp'] = (telemDict[i]['data'][4] << 8) + telemDict[i]['data'][5] 
					telemDict[i]['front pneumatic temp'] = (telemDict[i]['data'][2] << 8) + telemDict[i]['data'][3] 
					telemDict[i]['front solenoid temp'] = (telemDict[i]['data'][0] << 8) + telemDict[i]['data'][1] 

			all_tensioner_id2 = [779]
			for i in pressure_id2:
				if telemDict[i]['data'] != None:
					telemDict[i]['back pneumatic temp'] = (telemDict[i]['data'][0] << 8) + telemDict[i]['data'][1] 

			BMS_arduino_id = [1306,1338]
			for i in BMS_arduino_id:
				if telemDict[i]['data'] != None:
					telemDict[i]['discharge enable'] = telemDict[i]['data'][1]
					telemDict[i]['charge enable'] = telemDict[i]['data'][0] 

			if (telemDict[1049]['data'] != None) or (telemDict[1065]['data'] != None) or (telemDict[249]['data'] != None) or (telemDict[265]['data'] != None):
				telemDict[1049]['distance'] = (telemDict[1049]['data'][1] << 8) + telemDict[1049]['data'][0]
				telemDict[1065]['distance'] = (telemDict[1065]['data'][1] << 8) + telemDict[1065]['data'][0]

				telemDict[249]['distance'] = (telemDict[249]['data'][1] << 8) + telemDict[249]['data'][0]
				telemDict[265]['distance'] = (telemDict[265]['data'][1] << 8) + telemDict[265]['data'][0]
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
	global pod # Grab global pod object

	# List of possible commands
	cmds = {'state': {'set': '', 'current': ''}}

	while True:
		data = await reader.read(1024) # Max number of bytes to read
		if not data: # If no commands, stop
			break

		try:
			# Try decoding data, otherwise ignore it
			cmd = data.decode('utf8').rstrip().lower().split(" ")
		except Exception as e:
			print(f"Caught exception: {e}")
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
		else:
			output = f"Invalid command: {' '.join(cmd)}"

		output = output + "\n" # Add a newline character to output for conveinience
		writer.write(output.encode('utf8'))

	writer.close()

# Broascast telemetry for telemetry server
async def broadcastTlm(reader, writer, freq = 5):
	global pod # Grab global pod object
	# Init telemetry dictionary
	global telemetry
	# telemetry = {'state': str(pod.state), 'distance': 0}
	telemetry['state'] = str(pod.state)

	# Primary process loop
	while True:
		if writer.is_closing():
			# Watch for the client to close
			break
		
		telemetry['state'] = str(pod.state)
		if str(pod.state) == 'Launching' or str(pod.state) == 'Coasting' or str(pod.state) == 'Braking':
			telemetry['distance'] = telemetry['distance'] + 1 # Sample data

		output = json.dumps(telemetry) # Serialize dictionary as json
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
	print("HIIIII")
	while True:
		for _ in range(10):
			# Wait for next message from AsyncBufferedReader
			msg = await reader.get_message()
			print("data")
			print(msg.data)
			print("Timestamp")
			print(msg.timestamp)
			# Delay response
			await asyncio.sleep(0.05)
		# Wait for last message to arrive
		await reader.get_message()
		print('Done!')
		await asyncio.sleep(1/freq)

		# Clean-up
		notifier.stop()
		can0.shutdown()







async def CAN_out(freq = 5):
	# global stateDict # Grab the state dictionary
	# global pod # Grab pod object
	# global telemetry
	while True:
		print(stateDict[str(pod.state)])
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
	global stateDict # Grab the state dictionary
	global pod # Grab pod object
	global telemetry

	server_ip = "192.168.0.7" # SpaceX telemetry machine
	server_port = 3000

	team_id = 4
	# Instantiate a socket object of family AF_INET and type DOCK_DGRAM
	spacexTlmSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	# Send data at rate specified by freq
	while True:
		position = 1000000
		velocity = 9001
		acceleration = 981
		status = stateDict[str(pod.state)]

		# Pack the string according to format BB7iI

		# Packet layout (from SpaceX)
		# team_id			 uint8  Identifier for the team, assigned by the
		#							organization. Required.
		# status			  uint8  Pod status, indicating the current state the pod
		#							is in. Required.
		# acceleration		int32  Acceleration in centimeters per second squared.
		#							Required.
		# position			int32  Position in centimeters. Required.
		# velocity			int32  Velocity in centimeters per second. Required.
		# battery_voltage	 int32  Battery voltage in millivolts. Optional
		# battery_current	 int32  Battery current in milliamps. Optional
		# battery_temperature int32  Battery temperature in tenths of a degree
		#							Celsius. Optional
		# pod_temperature	 int32  Pod temperature in tenths of a degree Celsius.
		#							Optional
		# stripe_count		uint32 Count of optical navigation stripes detected in
		#							the tube. Optional
		packet = struct.pack(">BB7iI", team_id, status, int(acceleration), int(position), int(velocity), 0, 0, 0, 0, int(position) // 3048)
		spacexTlmSocket.sendto(packet, (server_ip, server_port))
		
		# Sleep for 1/freq secs before sending another packet
		await asyncio.sleep(1/freq)


async def state_transistion(freq = 5):
	global stateDict
	global pod
	global telemetry
	global id_dict
	while True:

		# try:
		# 	if (telemDict[281]['temp'] > motor_temp_fault or 
		# 		telemDict[297]['temp'] > motor_temp_fault or 
		# 		telemDict[313]['temp'] > motor_temp_fault or 
		# 		telemDict[329]['temp'] > motor_temp_fault or 
		# 		telemDict[345]['temp'] > motor_temp_fault or 
		# 		telemDict[361]['temp'] > motor_temp_fault or 
		# 		telemDict[1305]['max batt temp'] > max_batt_temp or 
		# 		telemDict[1321]['max batt temp'] > max_batt_temp or 
		# 		telemDict[1337]['max batt temp'] > max_batt_temp or 
		# 		telemDict[1305]['max v'] > max_V or 
		# 		telemDict[1321]['max v'] > max_V or 
		# 		telemDict[1337]['max v'] > max_V or 
		# 		telemDict[1305]['min v'] < min_V or 
		# 		telemDict[1321]['min v'] < min_V or 
		# 		telemDict[1337]['min v'] < min_V or 
		# 		((telemDict[281]['rpm'] > 0 or 
		# 		telemDict[297]['rpm'] > 0 or 
		# 		telemDict[313]['rpm'] > 0 or 
		# 		telemDict[329]['rpm'] > 0 or 
		# 		telemDict[345]['rpm'] > 0 or 
		# 		telemDict[361]['rpm'] > 0) and 
		# 		(telemDict[537]['reed'] == True or 
		# 		telemDict[553]['reed'] == True or 
		# 		telemDict[569]['reed'] == True or 
		# 		telemDict[585]['reed'] == True or 
		# 		telemDict[601]['reed'] == True or 
		# 		telemDict[617]['reed'] == True)) or 
		# 		telemDict[1305]['current'] > max_Amp or  
		# 		telemDict[1321]['current'] > max_Amp or  
		# 		telemDict[1337]['current'] > max_Amp):# or TelemCommand == 'Fault'):
		# 		pod.trigger('fault')
		# except Exception as e:
		# 	print(f"Caught exception: {e}")


		if ((stateDict[str(pod.state)] == 'launching') & (telemetry['velocity'] >= 185)):
			pod.trigger('coasting')
		elif ((stateDict[str(pod.state)] == 'launching') & (telemetry['position'] >= 3520)):
			pod.trigger('braking')

		if ((stateDict[str(pod.state)] == 'coasting') & (telemetry['position'] >= 3520)):
			pod.trigger('braking')

		if ((stateDict[str(pod.state)] == 'braking') & (telemetry['position'] >= 5180 & telemetry['velocity'] <= 0.5)):
			pod.trigger('crawling')
		elif ((stateDict[str(pod.state)] == 'braking') & (telemetry['position'] <= 5180 & telemetry['velocity'] <= 0.5)):
			pod.trigger(SafeToApproach)

		if ((stateDict[str(pod.state)] == 'crawling') & (telemetry['position'] >= 5180)):
			pod.trigger('braking')

		# Need to add loss of comms fault, pressure faults

		# Sleep for 1/freq secs before sending another packet
		await asyncio.sleep(1/freq)


# # Pings SpaceX to ensure communication
# async def ping(freq = 4):
# 	# fill in with ping pong
# 	await asyncio.sleep(1/freq)

# Instantiate the FSM as pod & drop into Startup
async def init_pod():
	global pod
	pod = FSM()

async def main():
	IP = "192.168.0.6" # Pi's IP address

	print(f"Host name: {socket.gethostname()}")
	print(f"IP address: {IP}")

	# file = open("/home/pi/data_log.csv", "a")
	# file_open = True
	# i=0
	# if os.stat("/home/pi/data_log.csv").st_size == 0:
 #		file.write("All CAN data \n")





	# Gather asynchronous coroutines
	await asyncio.gather(
		init_pod(),
		cmd_server(IP, 5000),
		tlm_server(IP, 5001),
		spacex_tlm(),
		state_transistion(),
		updateTelemDict(),
		processTelem(),
		# CAN_out(),		   
		# printing(),
		# broadcastTlm(),
		# processNetCmds()
	)

asyncio.run(main())


# # Get the default event loop
# loop = asyncio.get_event_loop()
# # Run until main coroutine finishes
# loop.run_until_complete(async_read_CAN)
# loop.close()
