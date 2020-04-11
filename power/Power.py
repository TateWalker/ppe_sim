class Power():

	def __init__(self):
		self.powered_on = False
		# self.power_usage = 0.0
		self.total_power = 65 #kW
		self.available_power = self.total_power
		self.generating_power = False
		self.generation_rate = 0.0
		self.eco_mode = False
		self.battery_level = 100 # percent USES BATTERY DURING ECLIPSE ONLY
		self.power_usage = 0


	#getters
	# def getBattery():

	def getReport(self):
		print('\n-------Power-------\n')
		print('Powered on: {}'.format(self.powered_on))
		print('Power usage: {}W'.format(self.power_usage))
		print('\n----------------------------\n')

	


	#setters

	def powerOn(self):
		self.powered_on = True
		print('Power on')
		print('{} kW available'.format(self.available_power))
		
		
	def togglePowerSaving(self,eco_mode):
		print("Changing power saving from {} to {}.".format(eco_mode,not(eco_mode)))
		return not(eco_mode)

	#utils

	# def reroutePower():

