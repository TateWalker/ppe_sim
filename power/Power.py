import logging

logger = logging.getLogger(__name__)

class Power():

	def __init__(self):
		self.name = 'Power A'
		self.powered_on = False
		self.generating_power = False
		self.generation_rate = 415.5 #kWh
		self.battery_capacity = 170  #kWh
		self.available_power = self.generation_rate
		self.power_usage = 0
		self.distance = 0

	#getters
	# def getBattery():

	def getReport(self):
		print('\n-------Power-------\n')
		logger.info('{} powered on: {}'.format(self.name, self.powered_on))
		logger.info('Power usage: {}kWh'.format(self.power_usage))
		logger.info('Generating power: {}'.format(self.generating_power))
		print('\n----------------------------\n')

	#setters

	def setDistance(self, distance):
		self.distance = distance

	def powerOn(self):
		self.powered_on = True
		logger.info('Power on')
		logger.info('{} kWh available'.format(self.available_power))
		self.generating_power = True

		
		
	def calculateAvailablePower(self,subsystems):
		for i in subsystems:
			self.available_power-=i.power_usage
			logger.info('{} kWh available'.format(self.available_power))

	def eclipse(self):
		self.generating_power = False
		full_capacity = self.battery_capacity
		logger.info('Power generation paused')
		for i in subsystems:
			self.battery_capacity-=i.power_usage
		if self.battery_capacity/full_capacity < .2:
			logger.warning('Battery less than 20\% capacity!')
		else:
			logger.info('Battery at {}\% capacity'.format(self.battery_capacity/full_capacity*100))