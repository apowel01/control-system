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

telemetry = dict()
telemetry['distance'] = 0

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
# New telemetry dictionary
telemDict = {
	281 or 'FR Motor': {
		'name': 	'FR Motor data',
		'data': 	0,
		'time': 	0,
		'rpm' : 	0,
		'volt': 	0,
		'temp': 	0,
		'throttle': 0,
		'torque': 0
		},
	297 or 'FL Motor': {
		'name': 'FL Motor data',
		'data': 	0,
		'time': 	0,
		'rpm' : 	0,
		'volt': 	0,
		'temp': 	0,
		'throttle': 0,
		'torque': 0
		},
	313 or 'MR Motor': {
		'name': 'MR Motor data',
		'data': 	0,
		'time': 	0,
		'rpm' : 	0,
		'volt': 	0,
		'temp': 	0,
		'throttle': 0,
		'torque': 0
		},
	329 or 'ML Motor': {
		'name': 'ML Motor data',
		'data': 	0,
		'time': 	0,
		'rpm' : 	0,
		'volt': 	0,
		'temp': 	0,
		'throttle': 0,
		'torque': 0
		},
	345 or 'RR Motor': {
		'name': 'RR Motor data',
		'data': 	0,
		'time': 	0,
		'rpm' : 	0,
		'volt': 	0,
		'temp': 	0,
		'throttle': 0,
		'torque': 0
		},
	361 or 'RL Motor': {
		'name': 'RL Motor data',
		'data': 	0,
		'time': 	0,
		'rpm' : 	0,
		'volt': 	0,
		'temp': 	0,
		'throttle': 0,
		'torque': 0
		},
	537 or 'FR Brake': {
		'name': 'FR Brake data',
		'data': 0,
		'time': 0,
		'temp': 0,
		'reed': 0
		},
	554 or 'FL Brake': {
		'name': 'FL Brake data',
		'data': 0,
		'time': 0,
		'temp': 0,
		'reed': 0
		},
	569 or 'MR Brake': {
		'name': 'MR Brake data',
		'data': 0,
		'time': 0,
		'temp': 0,
		'reed': 0
		},
	585 or 'ML Brake': {
		'name': 'ML Brake data',
		'data': 0,
		'time': 0,
		'temp': 0,
		'reed': 0
		},
	601 or 'RR Brake': {
		'name': 'RR Brake data',
		'data': 0,
		'time': 0,
		'temp': 0,
		'reed': 0
		},
	617 or 'RL Brake': {
		'name': 'RL Brake data',
		'data': 0,
		'time': 0,
		'temp': 0,
		'reed': 0
		},
	793 or 'FR Tensioner': {
		'name': 'FR Tensioner data',
		'data': 0,
		'time': 0,
		'reed': 0
		},
	809 or 'FL Tensioner': {
		'name': 'FL Tensioner data',
		'data': 0,
		'time': 0,
		'reed': 0
		},
	825 or 'MR Tensioner': {
		'name': 'MR Tensioner data',
		'data': 0,
		'time': 0,
		'reed': 0
		},
	841 or 'ML Tensioner': {
		'name': 'ML Tensioner data',
		'data': 0,
		'time': 0,
		'reed': 0
		},
	857 or 'RR Tensioner': {
		'name': 'RR Tensioner data',
		'data': 0,
		'time': 0,
		'reed': 0
		},
	873 or 'RL Tensioner': {
		'name': 'RL Tensioner data',
		'data': 0,
		'time': 0,
		'reed': 0
		},
	1049 or 'F Lidar': {
		'name': 'F Lidar data',
		'data': 			0,
		'time': 			0,
		'distance' : 		0
		},
	1065 or 'R Lidar': {
		'name': 'R Lidar data',
		'data': 			0,
		'time': 			0,
		'distance' : 		0
		},
	249 or 'R Band': {
		'name': 'R Band data',
		'data': 			0,
		'time': 			0,
		'time_arduino' :	0
		},
	265 or 'L Band':{
		'name': 'L Band data',
		'data': 			0,
		'time': 			0,
		'time_arduino' : 	0
		},
	1305 or 'F BMS': {
		'name': 'F BMS data',
		'data': 0,
		'time': 0,
		'max batt temp' : 0,
		'max v' : 0,
		'min v' : 0,
		'current' : 0
		},
	1321 or 'M BMS': {
		'name': 'M BMS data',
		'data': 0,
		'time': 0,
		'max batt temp' : 0,
		'max v' : 0,
		'min v' : 0,
		'current' : 0
		},
	1337 or 'R BMS': {
		'name': 'R BMS data',
		'data': 0,
		'time': 0,
		'max batt temp' : 0,
		'max v' : 0,
		'min v' : 0,
		'current' : 0
		},
	1306 or 'F BMS Arduino': {
		'name': 'F BMS Arduino data',
		'data': 	0,
		'time': 	0,
		'health' :  0
		},
	1322 or 'M BMS Arduino': {
		'name': 'M BMS Arduino data',
		'data': 	0,
		'time': 	0,
		'health' :  0
		},
	1338 or 'R BMS Arduino': {
		'name': 'R BMS Arduino data',
		'data': 	0,
		'time': 	0,
		'health' :  0
		}
	}


async def updateTelemDict(freq = 10):
	try:
		# timer = time.time()
		motor_id = [281,297,345,361]
		for i in motor_id:		
			telemDict[i]['rpm'] = telemDict[i]['data'][1] << 8 or telemDict[i]['data'][0]
			telemDict[i]['volt'] = telemDict[i]['data'][3] << 8 or telemDict[i]['data'][2]
			telemDict[i]['temp'] = telemDict[i]['data'][5] << 8 or telemDict[i]['data'][4]
			telemDict[i]['throttle'] = telemDict[i]['data'][6]
			
		brake_id = [537, 554, 601, 617]
		for i in brake_id:
			telemDict[i]['temp'] = telemDict[i]['data'][1] << 8 or telemDict[i]['data'][0]
			telemDict[i]['reed'] = telemDict[i]['data'][2]

		tension_id = [793, 809, 857, 873]
		for i in tension_id:
			telemDict[i]['reed'] = telemDict[i]['data'][0]
		
		telemDict[1049][distance] = telemDict[1049]['data'][1] << 8 or telemDict[1049]['data'][0]
		telemDict[1065][distance] = telemDict[1065]['data'][1] << 8 or telemDict[1065]['data'][0]

		telemDict[249][distance] = telemDict[249]['data'][1] << 8 or telemDict[249]['data'][0]
		telemDict[265][distance] = telemDict[265]['data'][1] << 8 or telemDict[265]['data'][0]
		# print("****************************")
		# print(time.time() - timer)
		# print("****************************")
	except Exception as e:
		pass
		
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
async def broadcastTlm(reader, writer):
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

		await asyncio.sleep(.1) # Wait until sending telem update

	writer.close()






# Process CAN-based telemetry
# Input: Processing frequency [Hz]
async def processTelem(freq = 10):
	global telemDict # Bring in telemetry dictionary

	while True:
		print("Trying to read can?")
		for msg in can0:
			print("  Arbitration id")
			print(msg.arbitration_id)
			print("  Data")
			print(msg.data)
			print("  Timestamp")
			print(msg.timestamp)
			# print(telemDict.keys)
			try:
				telemDict[msg.arbitration_id]['data'] = msg.data
				telemDict[msg.arbitration_id]['time'] = msg.timestamp				
			except Exception as e:
				print(f"Caught exception: {e}")
				continue
		#await asyncio.sleep(1/freq)
		print("**Flag**")

			# print("**MESSAGE**")
			# print(telemDict[1306]['health'])
			# print("**WORKS**")
			
		await asyncio.sleep(1/freq)




# Coroutine for sending telemetry to SpaceX
# Input: Transmit frequency [Hz]
async def spacex_tlm(freq = 50):
	global stateDict # Grab the state dictionary
	global pod # Grab pod object
	global telemetry

	server_ip = "192.168.0.8" # SpaceX telemetry machine
	server_port = 3000

	team_id = 0
	# Instantiate a socket object of family AF_INET and type DOCK_DGRAM
	spacexTlmSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	# Send data at rate specified by freq
	while True:
		position = telemetry['distance']
		velocity = 9001
		acceleration = 9.81
		status = stateDict[str(pod.state)]

		# Pack the string according to format BB7iI

		# Packet layout (from SpaceX)
		# team_id             uint8  Identifier for the team, assigned by the
		#                            organization. Required.
		# status              uint8  Pod status, indicating the current state the pod
		#                            is in. Required.
		# acceleration        int32  Acceleration in centimeters per second squared.
		#                            Required.
		# position            int32  Position in centimeters. Required.
		# velocity            int32  Velocity in centimeters per second. Required.
		# battery_voltage     int32  Battery voltage in millivolts. Optional
		# battery_current     int32  Battery current in milliamps. Optional
		# battery_temperature int32  Battery temperature in tenths of a degree
		#                            Celsius. Optional
		# pod_temperature     int32  Pod temperature in tenths of a degree Celsius.
		#                            Optional
		# stripe_count        uint32 Count of optical navigation stripes detected in
		#                            the tube. Optional
		packet = struct.pack(">BB7iI", team_id, status, int(acceleration), int(position), int(velocity), 0, 0, 0, 0, int(position) // 3048)
		spacexTlmSocket.sendto(packet, (server_ip, server_port))
		
		# Sleep for 1/freq secs before sending another packet
		await asyncio.sleep(1/freq)


async def state_transistion(freq = 10):
	global stateDict
	global pod
	global telemetry
	global id_dict
	while True:

		if (telemDict[281]['temp'] > motor_temp_fault or 
			telemDict[297]['temp'] > motor_temp_fault or 
			telemDict[313]['temp'] > motor_temp_fault or 
			telemDict[329]['temp'] > motor_temp_fault or 
			telemDict[345]['temp'] > motor_temp_fault or 
			telemDict[361]['temp'] > motor_temp_fault or 
			telemDict[1305]['max batt temp'] > max_batt_temp or 
			telemDict[1321]['max batt temp'] > max_batt_temp or 
			telemDict[1337]['max batt temp'] > max_batt_temp or 
			telemDict[1305]['max v'] > max_V or 
			telemDict[1321]['max v'] > max_V or 
			telemDict[1337]['max v'] > max_V or 
			telemDict[1305]['min v'] < min_V or 
			telemDict[1321]['min v'] < min_V or 
			telemDict[1337]['min v'] < min_V or 
			((telemDict[281]['rpm'] > 0 or 
			telemDict[297]['rpm'] > 0 or 
			telemDict[313]['rpm'] > 0 or 
			telemDict[329]['rpm'] > 0 or 
			telemDict[345]['rpm'] > 0 or 
			telemDict[361]['rpm'] > 0) and 
			(telemDict[537]['reed'] == True or 
			telemDict[553]['reed'] == True or 
			telemDict[569]['reed'] == True or 
			telemDict[585]['reed'] == True or 
			telemDict[601]['reed'] == True or 
			telemDict[617]['reed'] == True)) or 
			telemDict[1305]['current'] > max_Amp or  
			telemDict[1321]['current'] > max_Amp or  
			telemDict[1337]['current'] > max_Amp):# or TelemCommand == 'Fault'):


	#Need to add loss of comms fault, pressure faults
			pod.trigger('fault')

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
 #        file.write("All CAN data \n")


	# Gather asynchronous coroutines
	await asyncio.gather(
		init_pod(),
		cmd_server(IP, 5000),
		tlm_server(IP, 5001),
		spacex_tlm(),
		state_transistion(),
		updateTelemDict(),
		processTelem()           # Put process telem last, it messes everything afterwards
		# broadcastTlm(),
		# processNetCmds()
	)

asyncio.run(main())


# # Get the default event loop
# loop = asyncio.get_event_loop()
# # Run until main coroutine finishes
# loop.run_until_complete(async_read_CAN)
# loop.close()
