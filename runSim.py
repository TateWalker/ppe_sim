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
import pandas as pd
from plotter import plotter

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
	power.powerOn()
	prop.MainPropOn()
	prop_df = pd.DataFrame({'Distance': prop.distance_arr,'Delta V':prop.Delta_V_arr})
	prop_df.to_csv('export/prop_data.csv',header=True)
	comms.powerOn()
	gnc.powerOn()
	
	return comms,gnc,power,prop_df

def runReports(subsystems):
	#we want to grab all reports at once
	for i in subsystems:
		i.getReport()

def calculateDistance(subsystems,new_distance): #do linspace instead
	[x.setDistance(new_distance) for x in subsystems] #synchronizes distance amongst subsystems

def main():
	initiateLogger()
	output_data = pd.DataFrame(columns=['Time','Distance','GNC Saturation %','Data Rate','Power Generation Rate','Delta Velocity'])
	comms,gnc,power,prop_df = bootSequence()
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
		output_data = output_data.append({'Time':mission_time,'Distance':comms.distance,'GNC Saturation %': gnc.sat_percent, 'Data Rate': comms.signal_strength_return, 'Power Generation Rate': power.generation_rate},ignore_index = True)
		time.sleep(1)
		mission_time+=6
		if mission_time==132:
			break
		else:
			i+=1

	output_data.to_csv('export/subsystem_output.csv',header=True)
	plotter(output_data,prop_df)
	comms.getFinalReport()
		




if __name__ == '__main__':
	main()
