 #script that runs the sim
import numpy as np
from communication.Communications import Communications
from gnc.GNC import GNC
from power.Power import Power
from propulsion.IonProp import IonProp
import time
import logging
import sys

def initiateLogger():
		# set up logging to file - see previous section for more details
	logging.basicConfig(level=logging.DEBUG,
	                    format='%(asctime)s %(name)-30s %(levelname)-8s %(message)s',
	                    datefmt='%H:%M:%S',
	                    filename='logs/ppe.log',
	                    filemode='w')
	logging.info('Logger initiated')
	console = logging.StreamHandler()
	console.setLevel(logging.INFO)
	formatter = logging.Formatter('%(message)s')
	console.setFormatter(formatter)
	logging.getLogger('').addHandler(console)

def bootSequence():
	#apply startup to every class
	comms = Communications()
	gnc = GNC()
	power = Power()
	prop = IonProp()

	power.powerOn()
	prop.powerOn()
	comms.powerOn()
	gnc.powerOn()
	
	return comms,gnc,power,prop

def runReports(subsystems):
	#we want to grab all reports at once
	for i in subsystems:
		i.getReport()

def setRandomStates(subsystems): #should we make this not random but cyclical? would need velocity for that
	orbit_range = np.linspace(356873,426452)
	[x.setDistance(np.random.choice(orbit_range)) for x in subsystems] #synchronizes distance amongst subsystems

def main():
	#detach, check systems,ion prop to orbit, shut off prop
	#look at threading to wait one second
	initiateLogger()
	comms,gnc,power,prop = bootSequence()
	subsystems = [comms,gnc,power,prop]
	runReports(subsystems)
	mission_time=0 #sec
	while(True):
		if mission_time%10 == 0:
			runReports(subsystems)
		setRandomStates(subsystems)
		#if distance = CERTAIN_DISTANCE FOR EVENT: do something
		power.calculateAvailablePower(subsystems)
		time.sleep(1)
		mission_time+=1
		print('T+',str(mission_time))

		




if __name__ == '__main__':
	main()


	#set wait for 1 second for gnc
	#need to make backup flight computers


	#if dist from earth > x
		#fire prop
