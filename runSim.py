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

def calculateDistance(subsystems,velocity):
	if subsystems[0].distance < 356873:
		velocity*=(-1)
		missionScenarios.closeToEarth()
	elif subsystems[0].distance>426452:
		velocity*=(-1)
		missionScenarios.farFromEarth()

	new_distance = subsystems[0].distance+velocity
	[x.setDistance(new_distance) for x in subsystems] #synchronizes distance amongst subsystems
	return velocity

def main():
	#detach, check systems,ion prop to orbit, shut off prop
	#look at threading to wait one second
	initiateLogger()
	comms,gnc,power,prop = bootSequence()
	subsystems = [comms,gnc,power,prop]
	runReports(subsystems)
	mission_time=0 #sec
	velocity = 5
	random_scenarios = [missionScenarios.visitingVehicle, missionScenarios.eclipse]
	while(True):
		if mission_time%10 == 0:
			runReports(subsystems)
		elif mission_time%15 == 0:
			chance = np.random.randint(0,101)
			broken_subsystem = subsystems[np.random.randint(0,4)]
			if chance > 70: missionScenarios.subsystemFail(broken_subsystem)
		elif mission_time%30 == 0:
			chance = np.random.randint(0,11)
			if chance > 9: np.random.choice(random_scenarios)
		# else: missionScenarios.routine()
		
		velocity = calculateDistance(subsystems,velocity) #might need to make velocity a property of each class
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


		#need to make backup computers
