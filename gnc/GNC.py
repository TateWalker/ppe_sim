class GNC:

    def __init__(self):
        self.powerOn = False
        self.pos_target = np.empty([3])
        self.pos_error = np.empty([3])
        self.current_attitude = np.empty([3])
        self.burn_time = 0.0
        self.thrustersOn = np.empy([16]) # 16 thrusters needed   placeholder until we figure out exactly how many thrusters
        self.thrustMag = 5 # N   placeholder
        self.angDisp = np.empty([3])
        self.power_usage = 0




# setters

    def powerOn():
        self.powerOn = True

    def watchAttitude(self):
        for i in range(len(pos_error)):
            if self.pos_error[i] > 0.087266: #rad (5 deg)
                for i in range(len(thrustersOn[1])):
                  # set roll thrusters equal to 1
                  self.thrustersOn[2] = 1
                  self.thrustersOn[4] = 1 # etc.... to be decided later


    def FireThruster(self):
        for i in range(len(thrustersOn)):
            if self.thrustersOn[i] == 1:
                 self.burn()


    def burn(self):
        for i in range(len(pos_error)):
            while self.pos_error[i] > 0.087266:
                self.burn_time += 0.1
              # these should all be 3dVectors
              # torque[i] = r cross F    where r is 3dVector dist from thrust to origin of cube
              # alpha[i] = inv(I_mat)*torque     must find matrix of inertia for this (but its a cube so its super easy)
              # omega[i] = alpha*self.burn_time       get angular position by integrating
                for i in range(len(angDisp)):
                    print('Angular Displacement: {}'.format(self.angDisp[i]))
                    self.pos_error[i] = self.pos_error[i] - angDisp[i]
        for j in range(len(thrustersOn)):
            self.thrustersOn[j] = 0 # turn thrusters off


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

