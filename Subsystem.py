# Subsystem.py

class Subsystem:
	DEFAULT_POWER_STATUS = False
	DEFAULT_POWER_USAGE = 0.0
	DEFAULT_STABILITY = False

	'''
	Parent class for all subsystems. Defines default values for each subsystem.
	'''
	def __init__(self,name)
		self.powered_on = DEFAULT_POWER_STATUS
		self.power_usage = DEFAULT_POWER_USAGE
		self.is_stable = DEFAULT_STABILITY
		self.name = name

	def reboot(self): #yield everything
		print('Received reboot signal')
		self.powered_on = DEFAULT_POWER_STATUS
		print('{} powered off...'.format(self.name))
		self.power_usage = DEFAULT_POWER_USAGE
		self.is_stable = DEFAULT_STABILITY
		self.powerOn()
		print('{} powered on. Reconfiguring...'.format(self.name))


	def powerOn(self):
		self.powered_on = not(DEFAULT_POWER_STATUS)

	def getReport(self, subsystem):
		print('Get report from subsystem')

	def sendReport(self, subsystem):
		print('Send report to subsystem')
