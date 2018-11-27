# TELEMETRY

import numpy as np
import socket

class Telemetry():
	# team_id is an identifier for the team, assigned by SpaceX
	# Type UINT8
	# Total length of the payload of the packet is 34 bytes.

	self.teamID = 0
	self.maxFrameSpeed = 50
	self.minFrameSpeed = 10
	self.udpIP = "192.168.0.1"
	self.udpPort = "3000"

	def __init__(self):
		self.udpMessage = self.create_packet()
		return

	def get_status(self):
		# Pod status which FSM state is it in? This is for SpaceX's designated states, NOT OURS!!
		# Type UINT8
		stat = 0
		status = np.uint8(stat)
		return status

	def get_position(self):
		# Pod position estimation in centimeters from starting position
		# Type INT32
		pos = 0
		poition = np.int32(pos)
		return position

	def get_velocity(self):
		# Pod velocity estimation in cm/sec
		# Type INT32
		vel = 0
		velocity = np.int32(vel)
		return velocity

	def get_acceleration(self):
		# Pod acceleration estimation in cm/sec^2
		# Type INT32
		accel = 0
		acceleration = np.int32(accel)
		return acceleration

	def get_battery_voltage(self):
		# Battery voltage in mV
		# Type INT32
		voltage = 0
		batteryVoltage = np.int32(voltage)
		return batteryVoltage

	def get_battery_current(self):
		# Battery current in mA
		# Type INT32
		current = 0
		batteryCurrent = np.int32(current)
		return batteryCurrent

	def get_battery_temperature(self):
		# Battery temperature in 1/10ths of degrees C
		# Type INT32
		temp = 0
		batteryTemp = np.int32(temp)
		return

	def get_pod_temperature(self):
		# Pod temperature in 1/10ths of degrees C
		# Type INT32
		temp = 0
		podTemp = np.int32(temp)
		return podTemp

	def get_stripe_count(self):
		# Count of optical navigation stripes detected in the tube
		# Type UINT32
		stripes = 0
		stripeCount = np.uint32(stripes)
		return stripeCount

	def create_packet(self):
		# Binary telemetry frame to SpaceX computer for displaying
		# live pod information during the competition. 
		# at no greater than 50 Hz and no slower than 10 Hz.
		msg = []
		msg.append(self.teamID)
		msg.append(self.get_status)
		msg.append(self.get_position)
		msg.append(self.get_velocity)
		msg.append(self.get_acceleration)
		msg.append(self.get_battery_voltage)
		msg.append(self.get_battery_current)
		msg.append(self.get_battery_temperature)
		msg.append(self.get_stripe_count)
		return msg

	def send_packet(self):
		return




