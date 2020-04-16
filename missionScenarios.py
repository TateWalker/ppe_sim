import logging

logger = logging.getLogger(__name__)

def routine(subsystems):
	comms,gnc,power,prop = subsystems
	gnc.CmgWheel() # this does not seem to be called 
	

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
