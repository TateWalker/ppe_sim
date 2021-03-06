import pandas as pd
import numpy as np
import random
import math
import logging

logger = logging.getLogger(__name__)


data = pd.read_csv('gnc/ppe_mass_prop.csv')
df = pd.DataFrame(data, columns=['Mass', 'CoMX', 'CoMY', 'CoMZ', 'Ixx', 'Iyy', 'Izz', 'Ixy', 'Ixz', 'Iyz'])

thrusters = pd.read_csv('gnc/PPE_thruster_table_pythonformat.csv')

th = pd.DataFrame(thrusters, columns=['Xpos', 'Ypos', 'Zpos', 'Xdir', 'Ydir', 'Zdir', 'ThrustMag'])


th_Xpos = th['Xpos'].values
th_Ypos = th['Ypos'].values
th_Zpos = th['Zpos'].values
th_Xdir = th['Xdir'].values
th_Ydir = th['Ydir'].values
th_Zdir = th['Zdir'].values
th_mag = th['ThrustMag'].values


class GNC:

    def __init__(self):
        self.name = 'GNC A'
        self.powered_on = False
        self.burn_time = 0
        self.distance = 0.0
        self.thrustersOn = np.zeros(32)
        self.thrustMag = th_mag[0] # N
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
        self.torque_vec = np.zeros(3)
        self.lin_mom_vec = np.zeros(3)
        self.omega_vec = np.zeros(3)
        self.mom_capacity = 15000 #Nms
        self.base_slew_rate = 8.7266E-4 # rad/s based off 0.05 deg/s
        self.rev_per_s = 1.7745329E-6 # about 56 rev per 1 year
        self.desat_per_rev = 1.0
        self.fuel_per_desat = 0.042857 # kg
        self.rand_vec = np.zeros(3)
        self.mass_ship = 7478 # kg
        self.MomDiag = [25164.12, 30167.7, 43857.90] # Ixx, Iyy, Izz format
        self.desat_arr = []
        self.saturation = 0
        self.sat_percent = 0
        
        
               



# setters
    def setDistance(self, distance):
        self.distance = distance

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
        rand_alpha_a = min_torque_a / np.linalg.norm(self.MomDiag)  # in radians
        rand_alpha_p = max_torque_p / np.linalg.norm(self.MomDiag)
        rand_omega_a = rand_alpha_a  # assume the torque is exerted for 1 second
        rand_omega_p = rand_alpha_p  # assume the torque is exerted for 1 second

        rand_array = [1, 1, 1, 1, 1, 1, 1, 1, 0, 0]  # we are giving it an 80% chance to pick the smaller range, due to the highly eliptical orbit

        for i in range(len(self.rand_vec)):
            prob = random.randrange(0, 9)
            if rand_array[prob] == 1:
                self.rand_vec[i] = random.uniform(-rand_omega_a, rand_omega_a)
            else:
                self.rand_vec[i] = random.uniform(-rand_omega_p, rand_omega_p)

    def powerOn(self):
        self.powered_on = True
        self.power_usage = 800/1000 # W # could also get a rough power value from the amount of torque generated


    def DesatOMM(self):
        self.desat_arr.append(1)
        alpha = (self.thrustMag * self.CoM_to_thruster) / np.linalg.norm(self.MomDiag)# this is the ang acc imposed by each thruster. for our purposes, alpha = omega

        ### positive roll maneuver ###
        if self.omega_vec[0] < 5 * self.base_slew_rate:
            for i in range(len(self.pos_roll)):
                if self.thrustersOn[self.pos_roll[i]-1] < 1:
                    self.thrustersOn[self.pos_roll[i]-1] = 1 # minus one to fix index (there is no "zero" thruster)
                    logger.info('Thruster {} is on' .format(self.pos_roll[i]-1))

        while self.omega_vec[0] < 5 * self.base_slew_rate:
            self.omega_vec[0] = self.omega_vec[0] + (alpha * len(self.pos_roll)) # in rad, based off 0.1 deg/s, also arbitrary



        ### negative roll maneuver ###
        if self.omega_vec[0] > 5 * self.base_slew_rate:
            for i in range(len(self.neg_roll)):
                if self.thrustersOn[self.neg_roll[i]-1] < 1:
                    self.thrustersOn[self.neg_roll[i]-1] = 1 # minus one to fix index (there is no "zero" thruster)
                    logger.info('Thruster {} is on' .format(self.neg_roll[i]-1))
        while self.omega_vec[0] > 5 * self.base_slew_rate:
            self.omega_vec[0] = self.omega_vec[0] - (alpha * len(self.neg_roll)) # in rad, based off 0.1 deg/s, also arbitrary



        ### positive pitch maneuver ###
        if self.omega_vec[1] < 5 * self.base_slew_rate:
            for i in range(len(self.pos_pitch)):
                if self.thrustersOn[self.pos_pitch[i]-1] < 1:
                    self.thrustersOn[self.pos_pitch[i]-1] = 1 # minus one to fix index (there is no "zero" thruster)
                    logger.info('Thruster {} is on' .format(self.pos_pitch[i]-1))

        while self.omega_vec[1] < 5 * self.base_slew_rate:
            self.omega_vec[1] = self.omega_vec[1] + (alpha * len(self.pos_pitch)) # in rad, based off 0.1 deg/s, also arbitrary



        ### negative pitch maneuver ###
        if self.omega_vec[1] > 5 * self.base_slew_rate:
            for i in range(len(self.neg_pitch)):
                if self.thrustersOn[self.neg_pitch[i]-1] < 1:
                    self.thrustersOn[self.neg_pitch[i]-1] = 1  # minus one to fix index (there is no "zero" thruster)
                    logger.info('Thruster {} is on'.format(self.neg_pitch[i] - 1))

        while self.omega_vec[1] > 5 * self.base_slew_rate:
            self.omega_vec[1] = self.omega_vec[1] - (alpha * len(self.neg_pitch))  # in rad, based off 0.1 deg/s, also arbitrary




        ### positive yaw maneuver ###
        if self.omega_vec[2] < 5 * self.base_slew_rate:
            for i in range(len(self.pos_yaw)):
                if self.thrustersOn[self.pos_yaw[i] - 1] == 0:
                    self.thrustersOn[self.pos_yaw[i] - 1] = 1  # minus one to fix index (there is no "zero" thruster)
                    logger.info('Thruster {} is on'.format(self.pos_yaw[i] - 1))

        while self.omega_vec[2] < 5 * self.base_slew_rate:
            self.omega_vec[2] = self.omega_vec[2] + (alpha * len(self.pos_yaw))  # in rad, based off 0.1 deg/s, also arbitrary



        ### negative yaw maneuver ###
        if self.omega_vec[2] > 5 * self.base_slew_rate:
            for i in range(len(self.neg_yaw)):
                if self.thrustersOn[self.neg_yaw[i] - 1] == 0:
                    self.thrustersOn[self.neg_yaw[i] - 1] = 1  # minus one to fix index (there is no "zero" thruster)
                    logger.info('Thruster {} is on'.format(self.neg_yaw[i] - 1))

        while self.omega_vec[2] > 5 * self.base_slew_rate:
            self.omega_vec[2] = self.omega_vec[2] - (alpha * len(self.neg_yaw))  # in rad, based off 0.1 deg/s, also arbitrary

        for j in range(len(self.thrustersOn)):
            self.thrustersOn[j] = 0
            


    def CmgWheel(self):
        for j in range(10):
            self.powerOn() # call the power function
            self.RandPerturbation() # call the perturbation function to set rand_perb
            for i in range(len(self.omega_vec)):
                self.omega_vec[i] = self.omega_vec[i] + self.base_slew_rate # add an average slew rate each second
                self.omega_vec[i] = self.omega_vec[i] + self.rand_vec[i] # add a random perturbation each second
                self.lin_mom_vec[i] = self.MomDiag[i]*self.omega_vec[i]
            self.saturation = np.linalg.norm(self.lin_mom_vec)
            self.sat_percent = self.saturation / self.mom_capacity
            if self.saturation > self.mom_capacity:
                self.DesatOMM()
            

# getters

    def CheckSaturation(self):
        logger.info('CMG saturation at {:2.2f} percent capacity'.format((np.linalg.norm(self.lin_mom_vec)/self.mom_capacity)*100))

    def getReport(self):
        print('\n------------------GNC Report------------------\n')
        logger.info('{} powered on: {}'.format(self.name, self.powered_on))
        logger.info('Total Power Usage is {:2.2f}kWh'.format(self.power_usage))
        logger.info('CMG Saturation at {:2.2f} Percent Capacity'.format((np.linalg.norm(self.lin_mom_vec)/self.mom_capacity)*100))
        logger.info('Total Angular Velocity: {:3.2f} rad/s'.format(np.linalg.norm(self.omega_vec)))
        logger.info('Desaturation Maneuvers Performed: {}'.format(sum(self.desat_arr)))
        print('\n---------------------------------------------\n')
