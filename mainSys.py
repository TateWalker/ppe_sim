import itertools
import random
import simpy


class PPE:

	def __init__(self, env):
		self.env = env

	def alert():
		print('Alert alert')

	def reboot():
		print('Set everything back to defaults')

	def systemsOn():
		print('Sent \'On\' signal to each subsystem. ')

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


class Communications(Subsystem):

	def __init__(self):
		self.signal_strength = 0.0 #Mbps
		self.connected = False
		self.encrypted = False


	#getters

	def getMessage(): #read from queue

	def getSignalStrength():

	#setters

	def powerOn(self):
		#overloaded method for comm specific

	def setPowerDraw(power_level):

	#utils

	def sendMessage(): #send to nowhere (NASA)

	def encryptData():

		encrypted = True
		print('Encrypted shit')

		return encrypted


class Power(Subsystem):

	def __init__(self):
		self.total_power = 100 # kW ??
		self.available_power = self.total_power
		self.generating_power = False
		self.generation_rate = 0.0
		self.eco_mode = False
		self.battery_level = 100 # percent


	#getters

	def getBattery():

	


	#setters

	def powerOn(self):
		#overloaded method for power specific

	def togglePowerSaving():
		print("Changing power saving from {} to {}.".format(eco_mode,not(eco_mode)))
		return not(eco_mode)

	#utils

	def reroutePower():



class GNC(Subsystem):

	def __init__(self):
		self.pos_target = np.empty([1 3])
		self.pos_error = np.empty([1 3])

	def verifyManeuver():
		print('wat')

	def powerOn(self):
		#overloaded method for gnc specific

	def impulseApplied():
		print('wat')


class Propulsion(Subsystem):

	def __init__(self):
		self.prop_mode = "FULL SPEED AHEAD"
		self.main_prop = True
		self.main_prop_burn_time = 0.0
		self.cathode_power = False

	#getters

	def verifyThrust():
		if thrust:
			print('Thrusting')
		else:
			print('Not thrusting')
	
	#setters

	def powerOn(self):
		#overloaded method for prop specific

	def toggleCathode():
		print("Changing cathode power from {} to {}.".format(cathode_power,not(cathode_power)))
		return not(eco_mode)

	def fireMain():
		print('Firing main')
		self.main_prop = True
		#increase burn time


class Thruster:

	activated = False
	burnTime = 0.0

	#getters

	def isActive():
		return activated

	def getBurnTime():
		return burnTime

	#setters

	def powerOn(self):
		#overloaded method for thruster specific
