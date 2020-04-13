import logging

logger = logging.getLogger(__name__)

class Power():

	def __init__(self):
		self.powered_on = False
		self.total_power = 65000 #W
		self.available_power = self.total_power
		self.generating_power = False
		self.generation_rate = 0.0
		self.eco_mode = False
		self.battery_level = 100 # percent USES BATTERY DURING ECLIPSE ONLY
		self.power_usage = 10
		self.distance = 0

	#getters
	# def getBattery():

	def getReport(self):
		print('\n-------Power-------\n')
		logger.info('Powered on: {}'.format(self.powered_on))
		logger.info('Power usage: {}W'.format(self.power_usage))
		print('\n----------------------------\n')

	


	#setters

	def setDistance(self, distance):
		self.distance = distance

	def powerOn(self):
		self.powered_on = True
		logger.info('Power on')
		logger.info('{} kW available'.format(self.available_power/1000))
		
		
	def togglePowerSaving(self):
		logger.info("Changing power saving from {} to {}.".format(self.eco_mode,not(self.eco_mode)))
		self.eco_mode = not(self.eco_mode)

	def calculateAvailablePower(self,subsystems):
		for i in subsystems:
			self.available_power = self.total_power-i.power_usage
	#utils

	# def reroutePower():

