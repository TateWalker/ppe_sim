#script that runs the sim

from communication.Communications import Communications

def main():
	distance = 10E5
	comms = Communications()
	comms.powerOn(distance)
	comms.getReport()

if __name__ == '__main__':
	main()