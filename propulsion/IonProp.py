# processes: main thrust, check altitude, kg ionized.

import random
import pandas as pd
from numpy import log
import logging

logger = logging.getLogger(__name__)

# constants
q = 1.60217663E-19  # charge constant in coulombs
n = 6.0221409E+23  # avocado's numba
cou = 6.241509074E+18  # 1 coulomb
mass_proton = 1.6726219E-27  # mass of a proton

# fuel data
# data = pd.read_csv ('propulsion/XenonData.csv')
# df = pd.DataFrame(data, columns=['FIE', 'Molar Mass', 'Density', 'MeltingPt', 'cHeat'])
fie = 1170
# fie = df['FIE'].values  # kJ/mol
# mol_mass = df['Molar Mass'].values  # g
mol_mass = 131.29
#rho = df['Density'].values  # g/L
rho = 5.851
melting_point = -111.8
# melting_point = df['MeltingPt'].values  # celsius
# c_heat = df['cHeat'].values  # J/(g*K)
c_heat = 0.158


class IonProp:

    def __init__(self):
        self.powered_on = False
        self.main_prop_burn_time = 0.0 # s
        self.mass_flow = 0.0 # kg/s
        self.mass_kg = 0.0 # kg
        self.power = 0.0 # kW
        self.volts = 0.0 # volts
        self.delta_v = 0.0 # m/s
        self.thrust = 0.0 # N
        self.power_usage = 0.0
        self.set_power_draw = 40 # change later


# setters


    def setDistance(self, distance):
        self.distance = distance

    def powerOn(self):
        print('\n')
        self.powered_on = True
        logger.info('Ion propulsion on')
        self.power = 12.5
        self.volts = 300
        self.setPowerDraw()
        self.kgIonized()
        logger.info('Preparing to fire...')
        self.fireMainProp()

    def setPowerDraw(self):
        self.power_usage = self.power


    def kgIonized(self):       #is it supposed to calculate these values everytime we run a report?
        # intrinsic properties
        self.mass_kg = (mol_mass / n) * 0.001  # kg
        mol_ionized = self.power / fie  # mol/s
        mass_ionized = mol_ionized * mol_mass * 0.001  # kg/s
        ion_probability = random.uniform(0.40,0.60)
        self.mass_flow = mass_ionized*ion_probability  # kg/s
        logger.info('Kg Ionized: {}'.format(round(self.mass_kg,2)))
        logger.info('Mass flow rate: {}'.format(round(self.mass_flow,2)))


    def fireMainProp(self): # use massflow or kg_ionizd here?
        vel_out = pow((2 * self.volts * q) / self.mass_kg, 0.5) # m/s
        mass_init = 5945  # initial mass of PPE in kg
        self.delta_v = vel_out*log(mass_init/(mass_init - self.mass_flow)) # is my notation correct here?    units: m/s
        self.thrust = mol_mass * mass_proton * vel_out * ((self.power * 1000) / self.volts) * cou  # Newtons  we may not need this value
        logger.info('Delta V: {}'.format(self.delta_v))
        logger.info('Thrust: {}'.format(self.thrust))



# getters
    def getReport(self):
        print('\n------------Ion Propulsion Report------------\n')
        logger.info('Firing: {}'.format(self.powered_on))
        logger.info('Power draw: {}'.format(self.power))
        self.kgIonized()
        self.fireMainProp()
        print('\n---------------------------------------------\n')

