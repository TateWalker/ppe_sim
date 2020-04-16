import logging

logger = logging.getLogger(__name__)

def closeToEarth():
	logger.info('PPE is too far from the moon. Decreasing velocity.')

def farFromEarth():
	logger.info('PPE is too close to the moon. Increasing velocity.')

def routine(subsystems):
	comms,gnc,power,prop = subsystems
	logger.info('Routine')

def insertionBurn():
	logger.info('Insertion burn')

def visitingVehicle():
	logger.info('Visiting vehicle')

def eclipse(power):
	logger.info('Entering eclipse')
	power.eclipse()


def subsystemFail(subsystem):
	if subsystem.name[-1] == 'A':
		new_name = subsystem.name[0:-1]+'B'
	elif subsystem.name[-1] == 'B':
		new_name = subsystem.name[0:-1]+'C'
	else:
		logger.critical('Critical malfunction! All {} computers are down!'.format(subsystem.name[0:-2]))
		exit()
	logger.warning('{} failed! {} has taken over.'.format(subsystem.name,new_name))
	subsystem.name = new_name
	subsystem.powerOn()