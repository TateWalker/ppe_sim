import logging

logger = logging.getLogger(__name__)

class Power():

	def __init__(self):
		self.name = 'Power A'
		self.powered_on = False
		self.total_power = 65000 #W
		self.available_power = self.total_power
		self.generating_power = False
		self.generation_rate = 0.0
		self.battery_level = 100 # percent USES BATTERY DURING ECLIPSE ONLY
		self.power_usage = 10
		self.distance = 0

	#getters
	# def getBattery():

	def getReport(self):
		print('\n-------Power-------\n')
		logger.info('{} powered on: {}'.format(self.name, self.powered_on))
		logger.info('Power usage: {}W'.format(self.power_usage))
		print('\n----------------------------\n')

	#setters

	def setDistance(self, distance):
		self.distance = distance

	def powerOn(self):
		self.powered_on = True
		logger.info('Power on')
		logger.info('{} kW available'.format(self.available_power/1000))
		
		
	def calculateAvailablePower(self,subsystems):
		for i in subsystems:
			self.available_power-=i.power_usage
			logger.info('{} kW available'.format(self.available_power/1000))

	def eclipse(self):
		self.generating_power = False
		logger.info('Power generation paused')
	

