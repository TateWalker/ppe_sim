import pylink

class Communications():

	#range between closest between the moon and farthest away

	#farthest = 65000000m from moon
	#closeset = 3233000m from moon

	def __init__(self):
		self.powered_on = False
		self.power_usage = 0.0
		self.is_stable = False
		self.signal_strength_forward = 0.0 #Mbps
		self.signal_strength_return = 0.0 #Mbps
		self.connected = False
		self.f_stable = False
		self.r_stable = False

	#getters

	def getMessage(self): #read from queue
		print('Got message')

	def getSignalStrength(self, distance):
		print('Forward signal strength = {} Mbps'.format(self.signal_strength_forward))
		print('Return signal strength = {} Mbps'.format(self.signal_strength_return))

	def getReport(self):
		print('\n-------Communications-------\n')
		print('Powered on: {}'.format(self.powered_on))
		print('Power usage: {}W'.format(self.power_usage))
		self.getSignalStrength(100)
		print('Stable connection: {}'.format(self.is_stable))
		if not(self.is_stable):
			self.measureStability()
		print('Connected: {}'.format(self.connected))
		print('\n----------------------------\n')


	#setters 

	def powerOn(self, distance):
		self.powered_on = True
		print('\nCommunications powered on')
		self.setPowerDraw(100.0)
		print('Establishing link...')
		self.getSignalStrength(100)
		self.measureStability()
		if self.is_stable:
			self.connected = True
			print('Connected')

	def setPowerDraw(self, power):
		self.power_usage = power
	
	def measureStability(self):
		if self.signal_strength_forward < 30:
			print('Forward signal unstable')
			self.f_stable = False
		else:
			self.f_stable = True

		if self.signal_strength_return < 75:
			print('Return signal unstable')
			self.r_stable = False
		else:
			self.r_stable = True
			
		if self.f_stable and self.r_stable:
			print('All communications stable')
			self.is_stable = True

	def sendMessage(self): #send to nowhere (NASA)
		print('Sent message, no response :/')
	