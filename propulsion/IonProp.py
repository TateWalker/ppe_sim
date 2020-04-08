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
data = pd.read_csv ('propulsion/XenonData.csv')
df = pd.DataFrame(data, columns=['FIE', 'Molar Mass', 'Density', 'MeltingPt', 'cHeat'])

FIE = df['FIE'].values  # kJ/mol
MolMass = df['Molar Mass'].values  # g
rho = df['Density'].values  # g/L
meltPt = df['MeltingPt'].values  # celsius
cHeat = df['cHeat'].values  # J/(g*K)



class IonProp:

    def __init__(self):
        self.powered_on = False
        self.main_prop_burn_time = 0.0 # s
        self.MassFlow = 0.0 # kg/s
        self.massKg = 0.0 # kg
        self.power = 0.0 # kW
        self.volts = 0.0 # volts
        self.DeltaVel = 0.0 # m/s
        self.thrust = 0.0 # N
        self.power_usage = 0.0
        self.SetPowerDraw = 40 # change later


# setters

    def powerOn(self):
        self.powered_on = True
        print('\nIon propulsion on')
        self.power = 12.5
        self.volts = 300
        self.setPowerDraw()
        self.kg_ionized()
        print('\nPreparing to fire...')
        self.FireMainProp()

    def setPowerDraw(self):
        self.power_usage = self.power


    def kg_ionized(self, env):
        # intrinsic properties
        self.massKg = (MolMass / n) * 0.001  # kg
        molIonz = self.power / FIE  # mol/s
        MassIonz = molIonz * MolMass * 0.001  # kg/s
        IonizProb = env.timeout(random.randint(0.40,0.60))
        self.MassFlow = MassIonz*IonizProb  # kg/s
        print('Kg Ionized: {}'.format(self.massKg))
        print('Mass flow rate: {}'.format(self.MassFlow))


    def FireMainProp(self): # use massflow or kg_ionizd here?
        while self.powerOn:
            VelOut = pow((2 * self.volts * q) / self.massKg, 0.5) # m/s
            massInit = 5945  # initial mass of PPE in kg
            self.DeltaVel = VelOut*log(massInit/(massInit - self.MassFlow)) # is my notation correct here?    units: m/s
            self.thrust = MolMass * massPro * VelOut * ((self.power * 1000) / self.volts) * cou  # Newtons  we may not need this value
            if not self.powerOn:
                 break
        print('Delta V: {}'.format(self.DeltaVel))
        print('Thrust: {}'.format(self.thrust))



# getters
    def getReport(self):
        print('\n------------Ion Propulsion Report------------\n')
        print('We firing boyz? {}'.format(self.powerOn))
        print('Power draw: {}'.format(self.power))
        self.kg_ionized(simpy.Environment)
        self.FireMainProp()
        print('\n---------------------------------------------\n')


#env = simpy.Environment()
#go = IonProp(env)
#env.run(until=500)
