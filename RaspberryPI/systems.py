# Control systems classes such as brakes, tensioners, etc
import piplates.RELAYplate as relay # PiPlates relay library
import can # Get the CAN-bus module
import canDict # Get the CAN dictionary for sake of readability

# Address of relay plate (0-7, set by jumper on plate)
relay_addr = 0

class brake(object):

	engage_rel_1 = 1 # Relay number for brake engage solenoid 1
	engage_rel_2 = 2 # Relay number for brake engage solenoid 2
	disengage_rel = 3 # Relay number for brake disengage solenoid

	def __init__(self):
		# self.temp = self.get_temp()
		pass

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

class motor(object):
	"""docstring for motor"""
	# Instantiate the CAN-bus object
	bus = can.interface.Bus(channel='can0', bustype='socketcan_native')

	def __init__(self):
		self.disableAll() # Initialize with zero throttle

	# Returns True/False based upon whether the system is 
	def isNominal(self):
		return True
	
	#Set all motors to zero torque
	def disableAll(self):
		try:
			msg = can.Message(arbitration_id=canDict.ids['All stop'],
                      data=[0, 0, 0, 0, 0, 0, 0, 0],
                      extended_id=False)
			self.bus.send(msg)
		except can.CanError:
			print("****MOTOR COMMAND ERROR****")
			raise

	# Sets all motors to max torque
	def maxTorqueAll(self):
		try:
			msg = can.Message(arbitration_id=canDict.ids['All max power'],
                      data=[0, 0, 0, 0, 0, 0, 0, 0],
                      extended_id=False)
			self.bus.send(msg)
		except can.CanError:
			print("****MOTOR COMMAND ERROR****")
			raise
	
	#Set all motors to specified torque (0-100)
	def setTorqueAll(self,torque):
		try:
			msg = can.Message(arbitration_id=canDict.ids['All set power'],
                      data=[0, 0, 0, 0, 0, 0, 0, torque],
                      extended_id=False)
			self.bus.send(msg)
		except can.CanError:
			print("****MOTOR COMMAND ERROR****")
			raise
	
	# REDUNDANT? Set motor throttle to percentage setting, 0-100%
	def setThrottle(self, setting):
		print("@TODO Transmit throttle message: {}".format(setting))
		return True

	#Set one motor to zero torque (1:6 = FR,FL,MR,ML,BR,BL)
	def disableOne(self,motorid):
		try:
			if motorid == 1:
				canid = canDict.ids['FR Motor stop']
			elif motorid == 2:
				canid = canDict.ids['FL Motor stop']
			elif motorid == 3:
				canid = canDict.ids['MR Motor stop']
			elif motorid == 4:
				canid = canDict.ids['ML Motor stop']
			elif motorid == 5:
				canid = canDict.ids['BR Motor stop']
			elif motorid == 6:
				canid = canDict.ids['BL Motor stop']
			msg = can.Message(arbitration_id=canid,
                      data=[0, 0, 0, 0, 0, 0, 0, 0],
                      extended_id=False)
			self.bus.send(msg)
		except can.CanError:
			print("****MOTOR COMMAND ERROR****")
			raise

	#Set one motor to max torque (1:6 = FR,FL,MR,ML,BR,BL)
	def maxTorqueOne(self,motorid):
		try:
			if motorid == 1:
				canid = 273
			elif motorid == 2:
				canid = 289
			elif motorid == 3:
				canid = 305
			elif motorid == 4:
				canid = 321
			elif motorid == 5:
				canid = 337
			elif motorid == 6:
				canid = 353
			msg = can.Message(arbitration_id=canid,
                      data=[0, 0, 0, 0, 0, 0, 0, 0],
                      extended_id=False)
			self.bus.send(msg)
		except can.CanError:
			print("****MOTOR COMMAND ERROR****")
			raise

	#Set one motor to specified torque (1:6 = FR,FL,MR,ML,BR,BL)		
	def setTorqueOne(self,motorid,torque):
		try:
			if motorid == 1:
				canid = 274
			elif motorid == 2:
				canid = 290
			elif motorid == 3:
				canid = 306
			elif motorid == 4:
				canid = 322
			elif motorid == 5:
				canid = 338
			elif motorid == 6:
				canid = 354
			msg = can.Message(arbitration_id=canid,
                      data=[0, 0, 0, 0, 0, 0, 0, torque],
                      extended_id=False)
			self.bus.send(msg)
		except can.CanError:
			print("****MOTOR COMMAND ERROR****")
			raise
	
	# Sets pod speed in miles/hr
	def setSpeed(self, setting):
		print("@TODO Determine how to implement MPH-based drive: {} MPH".format(setting))
		return True

class battery(object):
	"""docstring for battery"""

	frontContactor = 4 # Relay number for front contactor
	midContactor = 5 # Relay number for mid contactor
	rearContactor = 6 # Relay number for rear contactor

	def __init__(self):
		self.disable() # Ensure batteries are off at creation

	# Enables battery packs by closing contactors
	def enable(self):
		try:
			# Close front, mid, and rear contactors
			relay.relayON(relay_addr, self.frontContactor)
			relay.relayON(relay_addr, self.midContactor)
			relay.relayON(relay_addr, self.rearContactor)
		except:
			print("****BATTERY ERROR****")
			raise

	# Disables battery packs by opening contactors
	def disable(self):
		try:
			# Open front, mid, and rear contactors
			relay.relayOFF(relay_addr, self.frontContactor)
			relay.relayOFF(relay_addr, self.midContactor)
			relay.relayOFF(relay_addr, self.rearContactor)
		except:
			print("****BATTERY ERROR****")
			raise

class tensioner(object):
	"""docstring for tensioner"""

	tensRelay = 7 # Relay number for tensioner solenoid

	def __init__(self):
		self.disable() # Ensure tensioner is disabled at creation

	# Enables tensioner by engaging solenoid
	def enable(self):
		try:
			# Close front, mid, and rear contactors
			relay.relayON(relay_addr, self.tensRelay)
		except:
			print("****TENSIONER ERROR****")
			raise

	# Disables tensioner by disengaging solenoid
	def disable(self):
		try:
			# Open front, mid, and rear contactors
			relay.relayOFF(relay_addr, self.tensRelay)
		except:
			print("****TENSIONER ERROR****")
			raise
