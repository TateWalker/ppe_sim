#import pylink
import logging
import numpy as np
from communication import getLinkBudget
from communication import linkBudgetConstants
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
		self.signal_strength_return = 0.0 #Mbps
		self.connected = False
		self.distance = 0.0 #km
		self.f_stable = False
		self.r_stable = False

	#getters

	def getFinalReport(self):
		getLinkBudget.main()
		print('Final communication report in the export folder')

	def getSignalStrength(self):
		m = linkBudgetConstants.DOWNLINK
		self.signal_strength_return = m.max_bitrate_hz*m.allocation_hz/1e13 + float(np.random.uniform(-10,10))

	def getReport(self):
		logger.info('\n-------Communications-------\n')
		logger.info('{} powered on: {}'.format(self.name, self.powered_on))
		logger.info('Power usage: {}kWh'.format(self.power_usage))
		logger.info('Signal strength = {:2.3f} Mbps'.format(self.signal_strength_return))
		logger.info('Stable connection: {}'.format(self.is_stable))
		logger.info('Connected: {}'.format(self.connected))
		logger.info('\n----------------------------\n')


	#setters 

	def setDistance(self, distance):
		self.distance = distance

	def powerOn(self):
		print('\n')
		self.powered_on = True
		logger.info('Communications powered on')
		self.setPowerDraw(10/1000)
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

	
	def measureStability(self):
		if self.signal_strength_return < 20:
			logger.warning('Return signal unstable')
			self.r_stable = False
		else:
			self.r_stable = True	
			logger.info('Communications stable')
			self.is_stable = True
	
