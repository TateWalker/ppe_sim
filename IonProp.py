import numpy as np
import math
import cmath
import matplotlib.pyplot as plt
import pandas as pd

# inputs
print('Fuel Types:\n HELIUM = 0\n NEON = 1\n ARGON = 2\n KRYPTON = 3\n XENON = 4\n')
FuelType = 0# int(input('Please enter fuel type:\n'))
DeltaVel = 10000# int(input('Please enter your desired delta velocity in m/s\n'))

# constants
q = 1.60217663E-19  # charge constant in coulombs
n = 6.0221409E+23  # avocado's numba
OpPow = 12.5 # kW
OpVolt = 300  # volts
cou = 6.241509074E+18  # 1 coulomb
massPro = 1.6726219E-27  # mass of a proton

# fuel data
data = pd.read_csv (r'/Users/kendallmares/Downloads/FuelType.csv')
df = pd.DataFrame(data, columns=['Name', 'FIE', 'Cost/gram', 'Molar Mass', 'Density', 'MeltingPt', 'cHeat'])


FIE = df['FIE'].values.tolist()  # kJ/mol
cost = df['Cost/gram'].values.tolist()  # $/g
MolMass = df['Molar Mass'].values.tolist()  # g
rho = df['Density'].values.tolist()  # g/L
meltPt = df['MeltingPt'].values.tolist()  # celsius
cHeat = df['cHeat'].values.tolist()  # J/(g*K)


# def ion(FuelType, DeltaVel):

# intrinsic properties
massKg = (MolMass[FuelType]/n) * 0.001  # kg
molIonz = OpPow/FIE[FuelType] # mol/s
MassIonz = molIonz * MolMass[FuelType] * 0.001  # kg/s

# desired values
VelOut = pow((2*OpVolt*q)/massKg, 0.5)  # m/s
massInit = 7500  # initial mass of PPE in kg
massFuel = -massInit * (1 - math.exp(DeltaVel/VelOut)) * math.exp(-DeltaVel/VelOut)  # kg
thrust = MolMass[FuelType] * massPro * VelOut * ((OpPow * 1000) / OpVolt) * cou  # Newtons
TotCost = cost[FuelType] * massFuel * 1000  # total cost (where mass is in kg)


volume = (massFuel * 1000) / rho[FuelType] # L
joulToCool = massFuel * cHeat[FuelType] * 1000 * (700 - meltPt[FuelType])  # in joules. 700C is assumed to be the operating temperature


if FuelType != 4:
    massKgXe = (MolMass[1] / n) * 0.001
    molIonzXe = OpPow / FIE[1]  # mol/s
    MassIonzXe = molIonzXe * MolMass[1] * 0.001  # kg/s

    # desired values
    VelOutXe = pow((2 * OpVolt * q) / massKgXe, 0.5)  # m/s
    massInitXe = 7500  # initial mass of PPE in kg
    massFuelXe = -massInitXe * (1 - math.exp(DeltaVel / VelOutXe)) * math.exp(-DeltaVel / VelOutXe)  # kg
    thrustXe = MolMass[1] * massPro * VelOutXe * ((OpPow * 1000) / OpVolt) * cou  # Newtons
    TotCostXe = cost[1] * massFuelXe * 1000  # total cost (where mass is in kg)


    volumeXe = (massFuelXe * 1000) / rho[1]  # L
    joulToCoolXe = massFuelXe * cHeat[1] * 1000 * (700 - meltPt[4])

    # Final ratios & comparison
   # massRat = round((massFuel/massFuelXe) * 100, 2)
   # costRat = round((TotCost/TotCostXe) * 100, 2)
   # thrustRat = round((thrust/thrustXe) * 100, 2)
   # volRat = round((volume/volumeXe) * 100, 2)
   # joulRat = round((joulToCool/joulToCoolXe) * 100, 2)




  #  print('Heres how your fuel compares to Xenon:\nYou used', massRat, '% of the mass\nYou used', costRat, '% of the cost\nYou used', thrustRat, '% of the thrust\nYou used', volRat, '% of the volume')

else:
    print('Here are your outputs:\nMass of Fuel:', massFuel, 'kg\nTotal cost:', TotCost, 'Dollars\nThurst:', thrust, 'N\nVolume:', volume, 'L')


######### for plotting purposes #########
Xemass = 2841.558641
XeVout = 20998.60545
Xecost = 3409870.37
Xethrust = 1.199218295
XeVol = 485653.5021
Xejoul = 364470814.1

massRat2 = round((massFuel / Xemass) * 100, 2)
costRat2 = round((TotCost / Xecost) * 100, 2)
thrustRat2 = round((thrust / Xethrust) * 100, 2)
volRat2 = round((volume / XeVol) * 100, 2)
joulRat2 = round((joulToCool / Xejoul) * 100, 2)

# Final ratios & comparison
massRat = round((massFuelXe / Xemass) * 100, 2)
costRat = round((TotCostXe / Xecost) * 100, 2)
thrustRat = round((thrustXe / Xethrust) * 100, 2)
volRat = round((volumeXe / XeVol) * 100, 2)
joulRat = round((joulToCoolXe / Xejoul) * 100, 2)

labels = ['Mass (kg)', 'Cost ($,2018)', 'Thrust (N)', 'Volume (L)', 'Energy to Cool (J)']
fuelTest = [massRat2, costRat2, thrustRat2, volRat2, joulRat2]
fuel2 = [massRat, costRat, thrustRat, volRat, joulRat]

x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, fuelTest, width, label='Helium')
rects2 = ax.bar(x + width/2, fuel2, width, label='Neon')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Percentage')
ax.set_title('Helium and Neon Efficiency Evaluation')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()


def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


autolabel(rects1)
autolabel(rects2)

fig.tight_layout()

plt.show()







