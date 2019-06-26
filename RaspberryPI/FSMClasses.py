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

	def entry(self):
		# Re-initialize systems
		import systems # Import systems classes
		global brakes # Grab the global brakes variable

		try:
			brakes = systems.brake() # Instantiate a braking object
			brakes.engage() # Engage the brakes
		except:
			raise

	# Transition to Safe to Approach
	def trigger(self, event):
		if event == 'safe_to_approach':
			return SafeToApproach()
	
		return self

# State 1: Safe to Approach
class SafeToApproach(State):

	def entry(self):
		pass

	# Transition to Crawling
	def trigger(self, event):
		if event == 'crawling':
			return Crawling()

		return self

# State 2: Ready to Launch
class ReadyToLaunch(State):

	def entry(self):
		global brakes

		try:
			brakes.engage()
		except:
			return Fault()

	# Transition to Launching
	def trigger(self, event):
		if event == 'launching':
			return Launching()

		return self

# State 3: Launching
class Launching(State):

	def entry(self):
		global brakes

		try:
			brakes.disengage()
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

		return self

# State 4: Coasting
class Coasting(State):

	def entry(self):
		pass

	# Transition to Braking
	def trigger(self, event):
		if event == 'braking':
			return Braking()

		return self

# State 5: Braking
class Braking(State):

	def entry(self):
		pass

	# Transition to next state
	def trigger(self, event):
		# Transition to Crawling
		if event == 'crawling':
			return Crawling()
		# Transition to Safe to Approach
		elif event == 'safe_to_approach':
			return SafeToApproach()

		return self

# State 6: Crawling
class Crawling(State):

	def entry(self):
		pass

	# Transition to Braking
	def trigger(self, event):
		if event == 'braking':
			return Braking()

		return self

# State 7: Startup
class Startup(State):

	def entry(self):
		# Initialize systems
		import systems # Import systems classes
		global brakes # Grab the global brakes variable

		try:
			brakes = systems.brake() # Instantiate a braking object
			brakes.engage() # Engage the brakes
		except:
			# If above doesn't work, fault
			return Fault()

	# Transition to Ready to Launch
	def trigger(self, event):
		if event == 'ready_to_launch':
			return ReadyToLaunch()

		return self