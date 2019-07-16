# Classes necessary for doing the state machine

# Primary state machine
class FSM(object):

	# Initialize the components.
	def __init__(self):
		# Start with a default state.
		self.state = Startup()

	def trigger(self, event):
		"""
		This is the bread and butter of the state machine. Incoming events are
		delegated to the given states which then handle the event. The result is
		then assigned as the new state.
		"""

		# The next state will be the result of the trigger function.
		self.state = self.state.trigger(event)

# Base class for states
class State(object):

	# Code which runs when first entering state
	def __init__(self):
		print('Processing current state: {}'.format(str(self)))

		self.entry() # Run entry code

	# Function the state performs
	def do(self):
		pass

	# Handle events that are delegated to this State.
	def trigger(self, event):
		pass

	# Perform entry tasks for state
	def entry(self):
		pass

	# Leverages the __str__ method to describe the State.
	def __repr__(self):
		return self.__str__()

	# Returns the name of the State.
	def __str__(self):
		return self.__class__.__name__

# State 0: Fault
class Fault(State):
	# Re-initialize systems
	import systems # Import systems classes

	def entry(self):
		global brakes # Grab the global brakes variable
		global motors # Grab the global motors variable
		global batteries # Grab the global batteries variable
		global tensioners # Grab the global tensioners variable

		try:
			brakes = self.systems.brake() # Instantiates a braking object
			motors = self.systems.motor() # Instantiates a motor object and sets throttle to 0
			batteries = self.systems.battery() # Instantiates a battery object and disables packs
			tensioners = self.systems.tensioner() # Instantiates a tensioner object and disables them

			brakes.engage() # Engage brakes
			batteries.disable() # Disable batteries
			motors.disableAll() # Set motor throttle to 0
			tensioners.disable() # Disengage tensioners

		except Exception as e:
			# If above doesn't work, fault
			print("Caught exception: {}".format(e))
			raise

	# Transition to Safe to Approach
	def trigger(self, event):
		if event == 'safe_to_approach':
			return SafeToApproach()
	
		return self

# State 1: Safe to Approach
class SafeToApproach(State):

	def entry(self):
		global brakes # Grab the global brakes variable
		global motors # Grab the global motors variable
		global batteries # Grab the global batteries variable
		global tensioners # Grab the global tensioners variable

		try:
			brakes.engage()
			motors.disableAll()
			batteries.disable()
			tensioners.disable()
		except:
			return Fault()

	# Transition to Crawling
	def trigger(self, event):
		if event == 'crawling':
			return Crawling()
		elif event == 'fault':
			return Fault()
		return self

# State 2: Ready to Launch
class ReadyToLaunch(State):

	def entry(self):
		global brakes # Grab the global brakes variable
		global motors # Grab the global motors variable
		global batteries # Grab the global batteries variable
		global tensioners # Grab the global tensioners variable

		try:
			brakes.engage()
			motors.disableAll()
			batteries.enable()
			tensioners.enable()
		except:
			return Fault()

	# Transition to Launching
	def trigger(self, event):
		if event == 'launching':
			return Launching()
		elif event == 'fault':
			return Fault()
		return self

# State 3: Launching
class Launching(State):

	def entry(self):
		global brakes # Grab the global brakes variable
		global motors # Grab the global motors variable
		global batteries # Grab the global batteries variable
		global tensioners # Grab the global tensioners variable

		try:
			brakes.disengage() # Disengage batteries
			batteries.enable() # Enables batteries
			tensioners.enable() # Engages tensioners
			motors.maxTorqueAll() # Set motors to 100%
		except:
			return Fault()


	# Transition to next state
	def trigger(self, event):
		# Transition to Braking
		if event == 'braking':
			return Braking()
		# Transition to Coasting
		elif event == 'coasting':
			return Coasting()
		elif event == 'fault':
			return Fault()
		return self

	# Checks telemetry to ensure we're go for launch
	def goForLaunch(self):
		global brakes # Grab the global brakes variable

# State 4: Coasting
class Coasting(State):

	def entry(self):
		global brakes # Grab the global brakes variable
		global motors # Grab the global motors variable
		global batteries # Grab the global batteries variable
		global tensioners # Grab the global tensioners variable

		try:
			brakes.disengage() # Disengage batteries
			batteries.enable() # Enables batteries
			tensioners.enable() # Engages tensioners
			motors.disableAll() # Set motors to 0%
		except:
			return Fault()

	# Transition to Braking
	def trigger(self, event):
		if event == 'braking':
			return Braking()
		elif event == 'fault':
			return Fault()
		return self

# State 5: Braking
class Braking(State):

	def entry(self):
		global brakes # Grab the global brakes variable
		global motors # Grab the global motors variable
		global batteries # Grab the global batteries variable
		global tensioners # Grab the global tensioners variable

		try:
			brakes.engage() # Disengage batteries
			batteries.enable() # Enables batteries
			tensioners.enable() # Engages tensioners
			motors.disableAll() # Set motors to 0%
		except:
			return Fault()

	# Transition to next state
	def trigger(self, event):
		# Transition to Crawling
		if event == 'crawling':
			return Crawling()
		# Transition to Safe to Approach
		elif event == 'safe_to_approach':
			return SafeToApproach()
		elif event == 'fault':
			return Fault()

		return self

# State 6: Crawling
class Crawling(State):

	def entry(self):
		global brakes # Grab the global brakes variable
		global motors # Grab the global motors variable
		global batteries # Grab the global batteries variable
		global tensioners # Grab the global tensioners variable

		try:
			brakes.disengage() # Disengage batteries
			batteries.enable() # Enables batteries
			tensioners.enable() # Engages tensioners
			motors.setSpeed(10) # Set speed
		except:
			return Fault()

	# Transition to Braking
	def trigger(self, event):
		if event == 'braking':
			return Braking()
		elif event == 'fault':
			return Fault()
		return self

# State 7: Startup
class Startup(State):
	import systems # Import systems classes

	def entry(self):
		# Initialize systems
		global brakes # Grab the global brakes variable
		global motors # Grab the global motors variable
		global batteries # Grab the global batteries variable
		global tensioners # Grab the global tensioners variable

		try:
			brakes = self.systems.brake() # Instantiates a braking object
			motors = self.systems.motor() # Instantiates a motor object and sets throttle to 0
			batteries = self.systems.battery() # Instantiates a battery object and disables packs
			tensioners = self.systems.tensioner() # Instantiates a tensioner object and disables them

			brakes.engage() # Engage brakes

		except Exception as e:
			# If above doesn't work, fault
			print("Caught exception: {}".format(e))
			return Fault()

	# Transition to Ready to Launch
	def trigger(self, event):
		if event == 'ready_to_launch':
			return ReadyToLaunch()
		elif event == 'fault':
			return Fault()
		return self