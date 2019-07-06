#!/usr/bin/env python3.7
#### The FSM for the Raspberry Pi Control System ####

# Imports
import asyncio # Used for asynchronous functions
import socket # Used for network communications
from FSMClasses import FSM # Grabs the FSM object

# Command server
async def cmd_server(host, port):
	server = await asyncio.start_server(processNetwork, host, port)
	await server.serve_forever()

# Process network commands
async def processNetwork(reader, writer):
	# List of possible commands
	global pod
	cmds = {'state': {'set': '', 'current': ''}}

	while True:
		# writer.write("Hi".encode('utf8'))
		data = await reader.read(100) # Max number of bytes to read
		if not data: # If data doesn't work, ignore
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

# Instantiate the FSM as pod & drop into Startup
async def init_pod():
	global pod
	pod = FSM()

async def main():
	# Gather asynchronous coroutines
	await asyncio.gather(
		cmd_server('127.0.0.1', 5000),
		init_pod()
	)

asyncio.run(main())

# pod.trigger('ready_to_launch')
# pod.trigger('launching')
# pod.trigger('coasting')
# pod.trigger('braking')
# pod.trigger('crawling')
# pod.trigger('braking')
# pod.trigger('safe_to_approach')