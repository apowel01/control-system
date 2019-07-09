#!/usr/bin/env python3.7
#### The FSM for the Raspberry Pi Control System ####

# Imports
import os
import time
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

#-------------CAN NETWORK SETUP---------------
os.system("sudo /sbin/ip link set can0 up type can bitrate 500000")
time.sleep(0.1)

# Command server
async def cmd_server(host, port):
	server = await asyncio.start_server(processNetCmds, host, port)
	await server.serve_forever()

# Telemetry server
async def tlm_server(host, port):
	server = await asyncio.start_server(processTlm, host, port)
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

# Process telemetry for telemetry server
async def processTlm(reader, writer):
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

# Coroutine for sending telemetry to SpaceX
# Input: Transmit frequency [Hz]
async def spacex_tlm(freq = 50):
	global stateDict # Grab the state dictionary
	global pod # Grab pod object
	global telemetry

	server_ip = "192.168.0.7" # SpaceX telemetry machine
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

# Instantiate the FSM as pod & drop into Startup
async def init_pod():
	global pod
	pod = FSM()

async def main():
	IP = "192.168.0.6" # Pi's IP address

	print(f"Host name: {socket.gethostname()}")
	print(f"IP address: {IP}")

	# Gather asynchronous coroutines
	await asyncio.gather(
		init_pod(),
		cmd_server(IP, 5000),
		tlm_server(IP, 5001),
		spacex_tlm()
	)

asyncio.run(main())