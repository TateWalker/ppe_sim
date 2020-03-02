import pandas as pd
import numpy as np
from scipy.spatial.transform import Rotation

data = pd.read_csv (r'/Users/kendallmares/ppe_sim/gnc/ppe_mass_prop.csv')
df = pd.DataFrame(data, columns=['Mass', 'CoMX', 'CoMY', 'CoMZ', 'Ixx', 'Iyy', 'Izz', 'Ixy', 'Ixz', 'Iyz'])

thrusters = pd.read_csv(r'/Users/kendallmares/ppe_sim/gnc/PPE_thruster_table_pythonformat.csv')
th = pd.DataFrame(thrusters, columns=['Xpos', 'Ypos', 'Zpos', 'Xdir', 'Ydir', 'Zdir', 'ThrustMag'])

ppe_mass = df['Mass'].values
COMX = df['CoMX'].values
CoMY = df['CoMY'].values
CoMZ = df['CoMZ'].values
Ixx = df['Ixx'].values
Iyy = df['Iyy'].values
Izz = df['Izz'].values
Ixy = df['Ixy'].values
Ixz = df['Ixz'].values
Iyz = df['Iyz'].values

th_Xpos = th['Xpos'].values
th_Ypos = th['Ypos'].values
th_Zpos = th['Zpos'].values
th_Xdir = th['Xdir'].values
th_Ydir = th['Ydir'].values
th_Zdir = th['Zdir'].values
th_mag = th['ThrustMag'].values

# rot = Rotation.from_euler('z', 90, degrees=True)

InertiaMat = np.array([[df['Ixx'].values, df['Ixy'].values, df['Ixz'].values], [df['Ixy'].values, df['Iyy'].values, df['Iyz'].values], [df['Ixz'].values, df['Iyz'].values, df['Izz'].values]])

# initial rotation matrix, this is a placeholder
Init_CMat = np.array([[-0.0000000, -0.7071068,  0.7071068],[0.7071068, -0.5000000, -0.5000000], [0.7071068,  0.5000000,  0.5000000]])

# yet another placeholder
Init_position = np.array([[1, 1, 1], [1,1,1], [1,1,1]])

class GNC:

    def __init__(self):
        self.powerOn = False
        self.pos_target = np.empty([3])
        self.pos_error = np.empty([3])
        self.current_attitude = Init_CMat # to be updated
        self.burn_time = 0.0
        self.thrustersOn = np.empy([32])
        self.thrustMag = th_mag # N
        self.angDisp = np.empty([3])
        self.current_position = Init_position # to be updated
        self.thrusterPosition = np.array([th_Xpos, th_Ypos, th_Zpos])
        self.thrusterDirection = np.array([th_Xdir, th_Ydir, th_Zdir])
        self.angDisp = np.empty([3])
        self.power_usage = 0
        self.forceVecFill = np.empty([3])
        self.forceVec = np.empty([3])
        self.torqueVec = np.empthy([3])
        self.alphaVec = np.empthy([3])
        self.omegaVec = np.empthy([3])
        self.angDisp = np.empthy([3])


# setters

    def powerOn(self):
        self.powerOn = True

    def watchAttitude(self):
        for i in range(len(self.pos_error)):
            if self.pos_error[i] > 0.087266: #rad (5 deg) this is a placeholder
                for i in range(len(self.thrustersOn[1])):
                  # set roll thrusters equal to 1
                  self.thrustersOn[2] = 1
                  self.thrustersOn[4] = 1 # etc.... to be decided later


    def FireThruster(self):
        for i in range(len(self.thrustersOn)):
            while self.pos_error[i] > 0.087266:
                if self.thrustersOn[i] == 1:
                     self.burn()
        self.thrustersOn[j] = 0  # turn thrusters off

    def burn(self):
        # these should all be 3dVectors
        for i in range(len(self.pos_error)):
            self.burn_time += 0.1
            self.forceVecFill[i] = self.current_position[i] + self.thrusterPosition[i] # transformation matrix multiplication get Inertia mat of moon
            forceNorm = np.linalg.norm(self.forceVecFill)
            self.forceVec[i] = self.thrustMag * self.forceVecFill[i]/forceNorm
            self.torqueVec[i] = np.cross(self.thrusterPosition[i, :], self.forceVec[i])        #   transpse this where r is 3dVector dist from thrust to origin of cube
            self.alphaVec[:] = np.linalg.inv(InertiaMat) * self.torqueVec[:]    #must find matrix of inertia for this (but its a cube so its super easy)
            self.omegaVec[i] = self.alphaVec[i] * self.burn_time
            self.angDisp[i]= self.omegaVec[i] * self.burn_time # this is an average value
        for i in range(len(self.angDisp)):
            print('Angular Displacement: {}'.format(self.angDisp[i]))
            self.pos_error[i] = self.pos_error[i] - self.angDisp[i]



  #  def cmgSpin(self):
        #do cmg stuff


# getters

    def checkAttitude(self):
        print('Attitude Error: {}'.format(self.pos_error))

    def gncReport(self):
        print('\n------------GNC Report------------\n')
        for i in range(len(self.thrustersOn)):
            print('We firing boyz? {}'.format(self.thrustersOn[i]))
        for i in range(len(self.angDisp)):
            print('Angular Displacement: {}'.format(self.angDisp[i]))
            print('Angular velocity: {}'.format(self.omega[i]))
            print('Position Error: {}'.format(self.pos_error[i]))

        print('\n---------------------------------------------\n')

