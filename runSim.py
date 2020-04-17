 #script that runs the sim
import numpy as np
from communication.Communications import Communications
from gnc.GNC import GNC
from power.Power import Power
from propulsion.IonProp import IonProp
import time
import logging
import sys
import missionScenarios

def initiateLogger():
		# set up logging to file - see previous section for more details
	logging.basicConfig(level=logging.INFO,
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
	prop.Delta_V_arr

	power.powerOn()
	prop.MainPropOn()
	comms.powerOn()
	gnc.powerOn()
	
	return comms,gnc,power,prop

def runReports(subsystems):
	#we want to grab all reports at once
	for i in subsystems:
		i.getReport()

def calculateDistance(subsystems,new_distance): #do linspace instead
	[x.setDistance(new_distance) for x in subsystems] #synchronizes distance amongst subsystems

def main():
	initiateLogger()
	comms,gnc,power,prop = bootSequence()
	subsystems = [comms,gnc,power]
	runReports(subsystems)
	mission_time=0 #hrs
	distances = np.linspace(356873,426452,22)

	i = 0

	while(True):
		print(chr(27) + "[2J")
		logging.info('T+{} hours'.format(mission_time))
		runReports(subsystems)
		if mission_time%15 == 0:
			chance = np.random.randint(0,101)
			broken_subsystem = subsystems[np.random.randint(0,3)]
			if chance > 90: missionScenarios.subsystemFail(broken_subsystem)
		else: missionScenarios.routine(subsystems)
		if i == 20:
			missionScenarios.eclipse(power,subsystems)
		new_distance = distances[i]
		calculateDistance(subsystems,new_distance)
		time.sleep(1)
		mission_time+=6
		if mission_time==132:
			break
		else:
			i+=1

	comms.getFinalReport()
		




if __name__ == '__main__':
	main()
