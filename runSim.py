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
	comms.powerOn()
	gnc.powerOn()

	return comms,gnc,power,prop

def runReports(subsystems):
	#we want to grab all reports at once
	for i in subsystems:
		i.getReport()



def main():

	comms,gnc,power,prop = bootSequence()
	subsytems = [com,gnc,power,prop]
	runReports()
	_
	powerDraws = {
		'Communications':comms.power_usage,
		'GNC':gnc.power_usage,
		'Power':power.power_usage,
		'Propulsion':prop.power_usage
		}



	while True:

		distance = 10E5
		comms = Communications()
		comms.powerOn(distance)
		comms.getReport()

if __name__ == '__main__':
	main()