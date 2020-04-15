#import pylink
import pylink
import logging

logger = logging.getLogger(__name__)

class Communications():

	#range between closest between the moon and farthest away

	#farthest = 65000000m from moon
	#closeset = 3233000m from moon

	def __init__(self):
		self.name = 'Communications A'
		self.powered_on = False
		self.power_usage = 0.0
		self.is_stable = False
		self.signal_strength_forward = 0.0 #Mbps
		self.signal_strength_return = 0.0 #Mbps
		self.connected = False
		self.distance = 0.0 #km
		self.f_stable = False
		self.r_stable = False

	#getters

	def getMessage(self): #read from queue
		print('Got message')

	def getSignalStrength(self):
		print('Forward signal strength = {} Mbps'.format(self.signal_strength_forward))
		print('Return signal strength = {} Mbps'.format(self.signal_strength_return))

	def getReport(self):
		print('\n-------Communications-------\n')
		logger.info('Powered on: {}'.format(self.powered_on))
		logger.info('Power usage: {}W'.format(self.power_usage))
		self.getSignalStrength()
		logger.info('Stable connection: {}'.format(self.is_stable))
		logger.info('Connected: {}'.format(self.connected))
		print('\n----------------------------\n')


	#setters 

	def setDistance(self, distance):
		self.distance = distance

	def powerOn(self):
		print('\n')
		self.powered_on = True
		logger.info('Communications powered on')
		self.setPowerDraw(10)
		logger.info('Establishing link...')
		self.getSignalStrength()
		self.measureStability()
		if self.is_stable:
			self.connected = True
			logger.info('Connected')
		else:
			self.connected = False
			logger.warning('Not connected')

	def setPowerDraw(self, power):
		self.power_usage = power

	def setSignalStrength(self):
		signal_strength_forward = 1
		signal_strength_return = 2
	
	def measureStability(self):
		if self.signal_strength_forward < 30:
			logger.warning('Forward signal unstable')
			self.f_stable = False
		else:
			self.f_stable = True

		if self.signal_strength_return < 75:
			logger.warning('Return signal unstable')
			self.r_stable = False
		else:
			self.r_stable = True
			
		if self.f_stable and self.r_stable:
			logger.info('All communications stable')
			self.is_stable = True

	def sendMessage(self): #send to nowhere (NASA)
		print('Sent message, no response :/')
	
