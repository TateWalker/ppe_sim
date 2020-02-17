# processes: main thrust, check altitude, kg ionized.

import random
import pandas as pd
import simpy
from numpy import log

RandomSeed = 16
theSeed = random.seed(RandomSeed)

# constants
q = 1.60217663E-19  # charge constant in coulombs
n = 6.0221409E+23  # avocado's numba
cou = 6.241509074E+18  # 1 coulomb
massPro = 1.6726219E-27  # mass of a proton

# fuel data
data = pd.read_csv (r'/Users/kendallmares/Downloads/XenonData.csv')
df = pd.DataFrame(data, columns=['FIE', 'Molar Mass', 'Density', 'MeltingPt', 'cHeat'])

FIE = df['FIE'].values.tolist()  # kJ/mol
MolMass = df['Molar Mass'].values.tolist()  # g
rho = df['Density'].values.tolist()  # g/L
meltPt = df['MeltingPt'].values.tolist()  # celsius
cHeat = df['cHeat'].values.tolist()  # J/(g*K)


# placeholders
powerOn = True
power = 12.5 # kW   remember to divide by 4 (one for each thruster)
volts = 300  # volts

class IonProp:

    def __init__(self, env):
        self.env = env
        #self.FireProcess = env.process(self.FireMainThrust(self, env, kg_ionizd, power))
        #self.kg_ionizd = env.process(self.kg_ionizd(self, env, power))
        #self.watchAttitude = env.process(self.watchAttitude(self, env, ** bool is_stable **))

    def FireMainThrust(self, kg_ionizd, powerOn, power, volts): # use massflow or kg_ionizd here?
        while powerOn:
            VelOut = pow((2 * volts * q) / kg_ionizd[1], 0.5) # m/s
            massInit = 7500  # initial mass of PPE in kg
            DeltaVel = VelOut*log(massInit/(massInit-kg_ionizd[0])) # is my notation correct here?    units: m/s
            thrust = MolMass * massPro * VelOut * ((power * 1000) / volts) * cou  # Newtons  we may not need this value
            if powerOn == False:
                 break
        return DeltaVel, thrust

    def kg_ionizd(self, env, powerOn, power):
        # intrinsic properties
        massKg = (MolMass / n) * 0.001  # kg
        molIonz = power / FIE  # mol/s
        MassIonz = molIonz * MolMass * 0.001  # kg/s
        IonizProb = env.timeout(random.randint(0.40,0.60))
        MassFlow = MassIonz*IonizProb  # kg/s

        return MassFlow, massKg

   # def watchAttitude(self, ** bool is_stable ** ):
        # put in code to fire attitude thrusters



env = simpy.Environment()
go = IonProp(env)
env.run(until=500)