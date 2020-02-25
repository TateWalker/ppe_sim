data = pd.read_csv (r'/Users/kendallmares/ppe_sim/gnc/ppe_mass_prop.csv')
df = pd.DataFrame(data, columns=['Mass', 'CoMX', 'CoMY', 'CoMZ', 'Ixx', 'Iyy', 'Izz', 'Ixy', 'Ixz', 'Iyz'])


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

InertiaMat = numpy.array([[df['Ixx'].values, df['Ixy'].values, df['Ixz'].values], [df['Ixy'].values, df['Iyy'].values, df['Iyz'].values], [df['Ixz'].values, df['Iyz'].values, df['Izz'].values]])



class GNC:

    def __init__(self):
        self.powerOn = False
        self.pos_target = np.empty([1, 3])
        self.pos_error = np.empty([1, 3])
        self.current_attitude = np.empty([1, 3])
        self.burn_time = 0.0
        self.thrustersOn = np.empy([1, 16]) # 16 thrusters needed   placeholder until we figure out exactly how many thrusters
        self.thrustMag = 5 # N   placeholder
        self.angDisp = np.empty([1, 3])
        self.current_position([1, 3])
        self.thrusterPosition([16, 3])
        self.thrusterDirection([16, 3])


# setters
    def watchAttitude(self):
        for i in range(len(pos_error)):
            if self.pos_error[i] > 0.087266: #rad (5 deg) this is a placeholder
                for i in range(len(thrustersOn[1])):
                  # set roll thrusters equal to 1
                  self.thrustersOn[2] = 1
                  self.thrustersOn[4] = 1 # etc.... to be decided later


    def FireThruster(self):
        for i in range(len(thrustersOn)):
            while self.pos_error[i] > 0.087266:
                if self.thrustersOn[i] == 1:
                     self.burn()
        self.thrustersOn[j] = 0  # turn thrusters off

    def burn(self):
        # these should all be 3dVectors
        forceVecFill = np.empty([1, 3])
        forceVec = np.empty([1, 3])
        torqueVec = np.empthy([1, 3])
        alphaVec = np.empthy([1, 3])
        omegaVec = np.empthy([1, 3])
        angDisp = np.empthy([1, 3])
        for i in range(len(pos_error)):
            self.burn_time += 0.1
            forceVecFill[i] = self.current_position[i] + self.thrusterPosition[i] # transformation matrix multiplication get Inertia mat of moon
            forceNorm = numpy.linalg.norm(forceVecFill)
            forceVec[i] = self.thrustMag * forceVecFill[i]/forceNorm
            torqueVec[i] = numpy.cross(thrusterPosition[i, :], forceVec[i])        #   transpse this where r is 3dVector dist from thrust to origin of cube
            alphaVec[:] = numpy.linalg.inv(InertiaMat) * torqueVec[:]    #must find matrix of inertia for this (but its a cube so its super easy)
            omegaVec[i] = alphaVec[i] * self.burn_time
            angDisp[i]= omegaVec[i] * self.burn_time # this is an average value
        for i in range(len(angDisp)):
            print('Angular Displacement: {}'.format(self.angDisp[i]))
            self.pos_error[i] = self.pos_error[i] - angDisp[i]



  #  def cmgSpin(self):
        #do cmg stuff


# getters

    def checkAttitude(self):
        print('Attitude Error: {}'.format(self.pos_error))

    def gncReport(self):
        print('\n------------GNC Report------------\n')
        for i in range(len(thrustersOn)):
            print('We firing boyz? {}'.format(self.thrustersOn[i]))
        for i in range(len(angDisp)):
            print('Angular Displacement: {}'.format(self.angDisp[i]))
            print('Angular velocity: {}'.format(self.omega[i]))
            print('Position Error: {}'.format(self.pos_error[i]))

        print('\n---------------------------------------------\n')

