 #script that runs the sim

from communication.Communications import Communications
from gnc.GNC import GNC
from power.Power import Power
from propulsion.IonProp import IonProp

def bootSequence():
	#apply startup to every class
	comms = Communications()
	gnc = GNC()
	power = Power()
	prop = IonProp()

	power.powerOn()
	prop.powerOn()
	comms.powerOn(10E5)
	gnc.powerOn()
	
	return comms,gnc,power,prop

def runReports(subsystems):
	#we want to grab all reports at once
	for i in subsystems:
		i.getReport()



def main():

	comms,gnc,power,prop = bootSequence()
	subsystems = [comms,gnc,power,prop]
	runReports(subsystems)
	powerDraws = {
		'Communications':comms.power_usage,
		'GNC':gnc.power_usage,
		'Power':power.power_usage,
		'Propulsion':prop.power_usage
		}

		




if __name__ == '__main__':
	main()