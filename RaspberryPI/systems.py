# Control systems classes such as brakes, tensioners, etc
import piplates.RELAYplate as relay # PiPlates relay library

# Address of relay plate (0-7, set by jumper on plate)
relay_addr = 0

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
			return "engaged"
		# Check to see if disengaged
		elif self.get_bit(relay_state, self.disengage_rel - 1):
			# Brakes are actually disengaged
			return "disengaged"
		# Something else is going on... probably not a good thing
		else:
			# Brakes are in an unexpected configuration
			return "unexpected"

	# Engages brakes by de-energizing "disengage solenoid" and energizing "engage solenoids"
	def engage(self):
		try:
			relay.relayON(relay_addr, self.engage_rel_1) # Energize "engage solenoid 1"
			relay.relayON(relay_addr, self.engage_rel_2) # Energize "engage solenoid 1"
			relay.relayOFF(relay_addr, self.disengage_rel) # De-energize "disengage solenoid"
		except:
			print("****BRAKING ERROR****")
			raise

	# Disengages brakes by energizing "disengage solenoid" and de-energizing "engage solenoids"
	def disengage(self):
		try:
			relay.relayOFF(relay_addr, self.engage_rel_1) # Energize "engage solenoid 1"
			relay.relayOFF(relay_addr, self.engage_rel_2) # Energize "engage solenoid 1"
			relay.relayON(relay_addr, self.disengage_rel) # De-energize "disengage solenoid"
		except:
			print("****BRAKING ERROR****")
			raise