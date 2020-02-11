### SimPy Notes:

# "processes"
	# model active components
	# live in "environment"
	# interact w/ environment via "events"
	# described by "generators" (function or method)
		# "generators" create events and "yield" them
	# "suspends" after "event" "yielded"
	# "resumes" after "event" "triggered"


### Car Example
# Simulated car will either drive or park for some amt of time
# After starting to drive/park, will print current sim time

import SimPy

env = SimPy.Environment()
env.process(car(env))

def car(env):

	while True:

		print('Start parking at %d' % env.now)
		park_time = 5
		yield env.timeout(park_time)

		print('Start driving at %d' % env.now)
		drive_time = 2
		yield env.timeout(drive_time)


