#!/usr/bin/env python3.7
#### The FSM for the Raspberry Pi Control System ####

# Imports
import json
import asyncio # Used for asynchronous functions
import socket # Used for network communications
from FSMClasses import FSM # Grabs the FSM object

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
		data = await reader.read(100) # Max number of bytes to read
		if not data: # If no commands, stop
			break

		# Split command as a list
		cmd = data.decode('utf8').rstrip().split(" ")
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
	telemetry = {'state': str(pod.state), 'distance': 0}

	# Primary process loop
	while True:
		if writer.is_closing():
			# Watch for the client to close
			break
		
		telemetry['state'] = str(pod.state)
		telemetry['distance'] = telemetry['distance'] + 1 # Sample data

		output = json.dumps(telemetry) # Serialize dictionary as json
		writer.write(output.encode('utf8'))

		await asyncio.sleep(.1) # Wait until sending telem update

	writer.close()

# Instantiate the FSM as pod & drop into Startup
async def init_pod():
	global pod
	pod = FSM()

async def main():
	IP = "192.168.0.6" # socket.gethostbyname(socket.gethostname()) # Grab Pi's IP address

	print(f"Host name: {socket.gethostname()}")
	print(f"IP address: {IP}")

	# Gather asynchronous coroutines
	await asyncio.gather(
		cmd_server(IP, 5000),
		tlm_server(IP, 5001),
		init_pod()
	)

asyncio.run(main())

