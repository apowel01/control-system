# Hold variable classes for FSM
# Created by: Amberley Powell
# Date Created: 3/28/2019
# Last modified by:
# Date last modified:
# Notes:
import sys
sys.path.append('../')
# import HealthMCU # I think this refers to the health.py file
import health # A bunch of random helper functions (of dubious use)
import can # CAN bus library
import piplates.RELAYplate as relay # PiPlates relay library

states = {
	"start_up" : 7,
	"system_diagnostic" : 15,
	"safe_to_approach" : 1,
	"prepare_to_launch" : 4,
	"ready_to_launch" : 2,
	"launching" : 3,
	"coasting" : 4,
	"braking" : 5,
	"full_stop" : 9,
	"crawling" : 6,
	"power_off" : 11,
	"fault" : 0,
	"fault_braking" : 12,
	"fault_stop" : 13,
	"fault_diagnostic" : 14
	}

# Relay plate options
relay_addr = 0 # Address of relay plate (0-7, set by jumper on plate)

# The relay code assumes our motors are on relays 1-6, 7 unused
bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
msg = can.Message(arbitration_id=0x000, data=[0], extended_id=False)
bus.send(msg)

class motor(object):
		# Holds attribute information for all motor objects

		def __init__(self, addr, i=0, v=0, temp=0):
				self.i = HealthMCU.get_motor_current()
				self.v = HealthMCU.get_motor_voltage()
				self.heat = HealthMCU.get_motor_heat()

		def power_on(self):

				pass

		def get_current(self):
				pass

		def get_voltage(self):
				pass

		def get_temp(self):
				pass

		def power_on_check(self):
				pass

		def power_off(self):
				pass

class battery(object):
		# Holds attribute information for all battery objects

		def __init__(self, addr, i=0, v=0, temp=0):
				self.i = i
				self.v = v
				self.temp = temp

		def get_current(self):
				pass

		def get_voltage(self):
				pass

		def get_temp(self):
				pass

class brake(object):

	def __init__(self, temp=0):
		# self.temp = self.get_temp()
		pass

	engage_rel_1 = 1 # Relay number for brake engage solenoid 1
	engage_rel_2 = 2 # Relay number for brake engage solenoid 2
	disengage_rel = 3 # Relay number for brake disengage solenoid

	# Returns the value of the bit at the given position (for status function)
	# @TODO Move this to helper function library
	def get_bit(self,val,ind):
		return ((val&(1<<ind)) != 0)

	# Would probably return temperature of the brake pads?
	def get_temp(self):
		# interupt_test.get_break_tempurature()
		# return
		pass

	# Returns the status of the brakes (engaged, disengaged, unexpected)
	def status(self):
		relay_state = relay.relaySTATE(relay_addr) # Get the relay status

		print("@TODO Add brake sensor reading")

		# Check to see if engaged
		if (self.get_bit(relay_state, self.engage_rel_1 - 1) and self.get_bit(relay_state, self.engage_rel_2 - 1)):
			# Brakes are actually engaged
			print("@TODO: Add state machine feedback!")
			return "engaged"
		# Check to see if disengaged
		elif self.get_bit(relay_state, self.disengage_rel - 1):
			# Brakes are actually disengaged
			print("@TODO: Add state machine feedback!")
			return "disengaged"
		# Something else is going on... probably not a good thing
		else:
			# Brakes are in an unexpected configuration
			print("@TODO: Add state machine feedback!")
			return "unexpected"

	# Engages brakes by de-energizing "disengage solenoid" and energizing "engage solenoids"
	def engage(self):
		try:
			relay.relayON(relay_addr, self.engage_rel_1) # Energize "engage solenoid 1"
			relay.relayON(relay_addr, self.engage_rel_2) # Energize "engage solenoid 1"
			relay.relayOFF(relay_addr, self.disengage_rel) # De-energize "disengage solenoid"
		except:
			print("****BRAKING ERROR****")

		print("@TODO: Add state machine fault under exception!")

	# Disengages brakes by energizing "disengage solenoid" and de-energizing "engage solenoids"
	def disengage(self):
		try:
			relay.relayOFF(relay_addr, self.engage_rel_1) # Energize "engage solenoid 1"
			relay.relayOFF(relay_addr, self.engage_rel_2) # Energize "engage solenoid 1"
			relay.relayON(relay_addr, self.disengage_rel) # De-energize "disengage solenoid"
		except:
			print("****BRAKING ERROR****")

		print("@TODO: Add state machine fault under exception!")

class wheel(object):
		# just for tracking RPM

		def __init__(self,addr,rpm=0):
				self.rpm = self.get_rpm()

		def get_rpm(self):
				return get_rpm() # placeholder function

class contactor(object):
		# need more info on this
		def __init__(self, addr, placeholder=0):
				self.placeholder = placeholder
