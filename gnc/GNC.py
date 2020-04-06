import pandas as pd
import numpy as np
import random
import os
thrusters = pd.read_csv('GNC/PPE_thruster_table_pythonformat.csv')
th = pd.DataFrame(thrusters, columns=['Xpos', 'Ypos', 'Zpos', 'Xdir', 'Ydir', 'Zdir', 'ThrustMag'])

# we could use these to calculate more exact torque values 
th_Xpos = th['Xpos'].values
th_Ypos = th['Ypos'].values
th_Zpos = th['Zpos'].values
th_Xdir = th['Xdir'].values
th_Ydir = th['Ydir'].values
th_Zdir = th['Zdir'].values
th_mag = th['ThrustMag'].values

class GNC:

    def __init__(self):
        self.powered_on = False
        self.burn_time = 0
        self.thrustersOn = np.empty([32])
        self.thrustMag = th_mag # N
        self.CoM_to_thruster = 4 # meters
        self.thrusterPosition = np.array([th_Xpos, th_Ypos, th_Zpos])
        self.thrusterDirection = np.array([th_Xdir, th_Ydir, th_Zdir])
        self.pos_roll = np.array([1,5,9,13,17,21,25,29])
        self.neg_roll = np.array([3,7,11,15,19,23,27,31])
        self.pos_pitch = np.array([4,5,15,23,28,29])
        self.neg_pitch = np.array([7,12,13,20,21,31])
        self.pos_yaw = np.array([3,8,9,17,27,32])
        self.neg_yaw = np.array([1,11,16,19,24,25])
        self.power_usage = 0
        self.torque_vec = np.empty([3])
        self.lin_mom_vec = np.empty([3])
        self.omega_vec = np.empty([3])
        self.mom_capacity = 15000 #Nms
        self.base_slew_rate = 8.7266E-4 # rad/s based off 0.05 deg/s
        self.rev_per_s = 1.7745329E-6 # about 56 rev per 1 year
        self.desat_per_rev = 1.0
        self.fuel_per_desat = 0.042857 # kg
        self.rand_perb = 0
        self.radius_ship = 2 # meters
        self.mass_ship = 7000 # kg
        self.MomInert = (1 / 12) * self.mass_ship * (self.radius_ship ** 2)



# setters

    def RandPerturbation(self):
        # math
        G = 6.67428E-11
        mass_moon = 7.34767309E+22
        r_p = 3233000
        r_a = 65000000
        F_G_p = (G * mass_moon * self.mass_ship) / (r_p ** 2)
        F_G_a = (G * mass_moon * self.mass_ship) / (r_a ** 2)
        min_torque_a = ((0.05 * F_G_a) + F_G_a) * 1  # 1m is assumed min moment arm with a 5% increase in gravity gradient
        max_torque_p = ((0.2 * F_G_p) + F_G_p) * 5  # moment arm is 5m and 20% increase in gravity gradient
        rand_alpha_a = min_torque_a / self.MomInert  # in radians
        rand_alpha_p = max_torque_p / self.MomInert
        rand_omega_a = rand_alpha_a  # assume the torque is exerted for 1 second
        rand_omega_p = rand_alpha_p  # assume the torque is exerted for 1 second

        rand_array = [1, 1, 1, 1, 1, 1, 1, 1, 0, 0]  # we are giving it an 80% chance to pick the smaller range, due to the highly eliptical orbit
        prob = random.randrange(0,9)

        if rand_array[prob] == 1:
            self.rand_perb = random.uniform(-rand_omega_a, rand_omega_a)
        else:
            self.rand_perb = random.uniform(-rand_omega_p, rand_omega_p)

    def powerOn(self):
        self.powered_on = True
        self.power_usage =+ 800 # joules # could also get a rough power value from the amount of torque generated


    def DesatOMM(self):
        alpha = (self.thrustMag * self.CoM_to_thruster) / self.MomInert # this is the ang acc imposed by each thruster. for our purposes, alpha = omega
        ### positive roll maneuver ###
        if self.omega_vec[0] < 4 * self.base_slew_rate: # yeah this is kinda arbitrary
            for i in range(len(self.pos_roll)):
                self.thrustersOn[self.pos_roll[i]-1] = 1 # minus one to fix index (there is no "zero" thruster)
            self.omega_vec[0] =+  alpha * len(self.pos_roll) # in rad, based off 0.1 deg/s, also arbitrary
            if self.omega_vec[0] >= 4 * self.base_slew_rate: # checks to see if the attitude change is greater than our threshold. if so, turns thrusters off
                for i in range(len(self.pos_roll)):
                    self.thrustersOn[self.pos_roll[i]-1] = 0
            return # breaks the if statement
        ### negative roll maneuver ###
        if self.omega_vec[0] > 4 * self.base_slew_rate:
            for i in range(len(self.neg_roll)):
                self.thrustersOn[self.neg_roll[i]-1] = 1
            self.omega_vec[0] =- alpha* len(self.neg_roll)
            if self.omega_vec[0] <= 4 * self.base_slew_rate:
                for i in range(len(self.neg_roll)):
                    self.thrustersOn[self.neg_roll[i]-1] = 0
            return
        ### positive pitch maneuver ###
        if self.omega_vec[1] < 4 * self.base_slew_rate:
            for i in range(len(self.pos_pitch)):
                self.thrustersOn[self.pos_pitch[i]-1] = 1
            self.omega_vec[1] =+ alpha * len(self.pos_pitch)
            if self.omega_vec[1] >= 4 * self.base_slew_rate:
                for i in range(len(self.pos_pitch)):
                    self.thrustersOn[self.pos_pitch[i]-1] = 0
            return
        ### negative pitch maneuver ###
        if self.omega_vec[1] > 4 * self.base_slew_rate:
            for i in range(len(self.neg_pitch)):
                self.thrustersOn[self.neg_pitch[i]-1] = 1
            self.omega_vec[1] =- alpha * len(self.neg_pitch)
            if self.omega_vec[1] <= 4 * self.base_slew_rate:
                for i in range(len(self.neg_pitch)):
                    self.thrustersOn[self.neg_pitch[i]-1] = 0
            return
        ### positive yaw maneuver ###
        if self.omega_vec[2] < 4 * self.base_slew_rate:
            for i in range(len(self.pos_yaw)):
                self.thrustersOn[self.pos_yaw[i]-1] = 1
            self.omega_vec[2] =+ alpha * len(self.pos_yaw)
            if self.omega_vec[2] >= 4 * self.base_slew_rate:
                for i in range(len(self.pos_yaw)):
                    self.thrustersOn[self.pos_yaw[i]-1] = 0
            return
        ### negative yaw maneuver ###
        if self.omega_vec[2] > 4 * self.base_slew_rate:
            for i in range(len(self.neg_yaw)):
                self.thrustersOn[self.neg_yaw[i] - 1] = 1
            self.omega_vec[2] =- alpha * len(self.neg_yaw)
            if self.omega_vec[2] <= 4 * self.base_slew_rate:
                for i in range(len(self.neg_yaw)):
                    self.thrustersOn[self.neg_yaw[i] - 1] = 0
            return


    def CmgWheel(self):
        self.powerOn() # call the power function
        self.RandPerturbation() # call the perturbation function to set rand_perb
        for i in range(len(self.omega_vec)):
            self.omega_vec[i] =+ self.base_slew_rate # add an average slew rate each second
            self.omega_vec[i] =+ self.rand_perb # add a random perturbation each second
            self.lin_mom_vec[i] = self.MomInert*self.omega_vec[i]

        if np.linalg.norm(self.lin_mom_vec) > self.mom_capacity:
            self.DesatOMM()

# getters

    def CheckSaturation(self):
        print('CMG saturation at {} percent capacity'.format((np.linalg.norm(self.lin_mom_vec)/self.mom_capacity)*100))

    def GncReport(self):
        print('\n------------GNC Report------------\n')
        print('CMG saturation at {} percent capacity'.format((np.linalg.norm(self.lin_mom_vec)/self.mom_capacity)*100))
        print('Total power usage is {} kW'.format(self.power_usage/1000))
        for i in range(len(self.thrustersOn)):
            print('Thrusters firing: {}'.format(self.thrustersOn[i]))
        for i in range(len(self.pos_roll)):
            if self.thrustersOn[self.pos_roll[i]] == 1:
                print('Rolling in the positive direction at {} rad/s'.format(0.0017453 * len(self.pos_roll)))
            if self.thrustersOn[self.neg_roll[i]] == 1:
                print('Rolling in the negative direction at {} rad/s'.format(0.0017453 * len(self.neg_roll)))
        for i in range(len(self.pos_pitch)):
            if self.thrustersOn[self.pos_pitch[i]] == 1:
                print('Pitching in the positive direction at {} rad/s'.format(0.0017453 * len(self.pos_pitch)))
            if self.thrustersOn[self.neg_pitch[i]] == 1:
                print('Pitching in the negative direction at {} rad/s'.format(0.0017453 * len(self.neg_pitch)))
            if self.thrustersOn[self.pos_yaw[i]] == 1:
                print('Yawing in the positive direction at {} rad/s'.format(0.0017453 * len(self.pos_yaw)))
            if self.thrustersOn[self.neg_yaw[i]] == 1:
                print('Yawing in the negative direction at {} rad/s'.format(0.0017453 * len(self.neg_yaw)))
        for i in range(len(self.omega_vec)):
            print('Total Angular velocity: {}'.format(self.omega_vec[i]))


        print('\n---------------------------------------------\n')

