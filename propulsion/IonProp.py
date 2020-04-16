import random
import pandas as pd
from numpy import log


# constants

# fuel data
data = pd.read_csv (r'propulsion/XenonData.csv')
df = pd.DataFrame(data, columns=['FIE', 'Molar Mass', 'Density', 'MeltingPt', 'cHeat'])

FIE = df['FIE'].values # kJ/mol
MolMass = df['Molar Mass'].values  # g
rho = df['Density'].values # g/L
meltPt = df['MeltingPt'].values # celsius
cHeat = df['cHeat'].values  # J/(g*K)

class IonProp:

    def __init__(self):
        self.powerOn = False
        self.main_prop_burn_time = 0.0 # s
        self.MassFlow = 0.0 # kg/s
        self.massKg = 0.0 # kg
        self.power = 0.0 # kW
        self.volts = 0.0 # volts
        self.LifeTimeDeltaVel = 0.0 # m/s
        self.thrust = 0.0 # N
        self.SetPowerDraw = 40 # change later
        self.q = 1.60217663E-19  # charge constant in coulombs
        self.n = 6.0221409E+23  # avocado's numba
        self.cou = 6.241509074E+18  # 1 coulomb
        self.massPro = 1.6726219E-27  # mass of a proton
        self.DeltaV = 0
        self.distance = 0
        self.hours = 0
        self.mass_used = 0



# setters

    def MainPropOn(self):
        self.powerOn = True
        print('\nIon propulsion on')
        self.power = 12.5
        self.volts = 300
        while self.powerOn:
            self.kgIonized()
            self.FireMainProp()
            self.getReport()
            if 356870 - self.distance <= 0:
                self.powerOn = False
                print('\n Arrived at NRHO orbit')
                print('\n---------Final Ion Propulsion Report---------\n')
                print('Total Power Draw: {} kWh'.format(self.power * (self.hours - 1 + (self.distance - 356870) / self.DeltaV)))
                print('Total Ionized Mass: {} kg/s'.format(self.mass_used - (self.MassFlow*30)))
                print('Transit Time: {} hours'.format(self.hours - 1 + (self.distance - 356870) / self.DeltaV) )
                print('\n---------------------------------------------\n')



    def kgIonized(self):
        # intrinsic properties
        self.massKg = (MolMass / self.n) * 0.001  # kg
        molIonz = self.power / FIE  # mol/s
        MassIonz = molIonz * MolMass * 0.001  # kg/s this is assumed to be the value at 50% efficiency
        IonizProb = random.uniform(0.15,0.30) # our efficiency for this is 65-80 %
        self.MassFlow = MassIonz + MassIonz*IonizProb  # kg/s
        self.mass_used += (self.MassFlow*60)



    def FireMainProp(self): # use massflow or kg_ionizd here?
        VelOut = pow((2 * self.volts * self.q) / self.massKg, 0.5) # m/s
        massInit = 7478  # initial mass of PPE in kg
        self.DeltaV = ((VelOut/1000)*3600)*log(massInit/(massInit - (self.MassFlow*3600))) # assumed for 1 second
        self.LifeTimeDeltaVel = VelOut*log(massInit/(massInit - 2000)) # is my notation correct here?    units: m/s
        self.thrust = MolMass * self.massPro * VelOut * ((self.power * 1000) / self.volts) * self.cou  # Newtons  we may not need this values
        self.distance += self.DeltaV
        self.hours = self.hours + 1



# getters
    def getReport(self):
        print('\n------------Ion Propulsion Report------------\n')
        print('Power Draw: {}'.format(self.power))
        print('Ionized Mass Flow Rate: {} kg/s'.format(self.MassFlow))
        print('Current Delta V: {} km/hr'.format(self.DeltaV))
        print('Distance to Moon: {}'.format(356870 - self.distance))
        print('Time in Transit: {} hours'.format(self.hours))
        print('\n---------------------------------------------\n')
