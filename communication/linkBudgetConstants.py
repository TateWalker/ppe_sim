#!/usr/bin/env python

import os
import shutil
import subprocess
import numpy as np
import matplotlib.pyplot as plt

import pylink



sat_pattern = pylink.pattern_generator(3)


sat_rf_chain = [
  pylink.Element(name='Cables',
                 gain_db=-0.75,
                 noise_figure_db=0.75),
  pylink.Element(name='LNA',
                 gain_db=35,
                 noise_figure_db=2.75),
  pylink.Element(name='Filter',
                 gain_db=-3.5,
                 noise_figure_db=3.5),
  pylink.Element(name='Demodulator',
                 gain_db=0,
                 noise_figure_db=15),
  ]

gs_rf_chain = [
  pylink.Element(name='Cables',
                 gain_db=-0.75,
                 noise_figure_db=0.75),
  pylink.Element(name='LNA',
                 gain_db=35,
                 noise_figure_db=2.75),
  pylink.Element(name='Filter',
                 gain_db=-3.5,
                 noise_figure_db=3.5),
  pylink.Element(name='Demodulator',
                 gain_db=0,
                 noise_figure_db=15),
  ]

geometry = pylink.Geometry(apoapsis_altitude_km=426452,
                         periapsis_altitude_km=356873,
                         min_elevation_deg=20)

sat_rx_antenna = pylink.Antenna(gain=54.7,
                              polarization='RHCP',
                              pattern=sat_pattern,
                              rx_noise_temp_k=288.84,
                              is_rx=True,
                              tracking=False)

sat_tx_antenna = pylink.Antenna(gain=53.11,
                                polarization='RHCP',
                                pattern=sat_pattern,
                                is_rx=False,
                                tracking=False)

gs_rx_antenna = pylink.Antenna(pattern=pylink.pattern_generator(48),
                               rx_noise_temp_k=25.6,
                               polarization='LCP',
                               is_rx=True,
                               tracking=True)

gs_tx_antenna = pylink.Antenna(gain=79,
                               polarization='LCP',
                               is_rx=False,
                               tracking=True)

sat_receiver = pylink.Receiver(rf_chain=sat_rf_chain,
                               implementation_loss_db=2,
                               name='Satellite Ka-Band Receiver')

gs_receiver = pylink.Receiver(rf_chain=gs_rf_chain,
                              name='Ground Ka-Band Receiver')

gs_transmitter = pylink.Transmitter(tx_power_at_pa_dbw=25,
                                    name='Ground Ka-Band Transmitter')

sat_transmitter = pylink.Transmitter(tx_power_at_pa_dbw=50,
                                     name='Satellite Ka-Band Transmitter')

rx_interconnect = pylink.Interconnect(is_rx=True)


tx_interconnect = pylink.Interconnect(is_rx=False)


ka_channel = pylink.Channel(bitrate_hz=.072,
                           allocation_hz=500e6,
                           center_freq_mhz=32550,
                           atmospheric_loss_db=1,
                           ionospheric_loss_db=1,
                           rain_loss_db=2,
                           multipath_fading_db=0,
                           polarization_mismatch_loss_db=3)

modulation = pylink.Modulation()


DOWNLINK = pylink.DAGModel([geometry,
                          gs_rx_antenna,
                          sat_transmitter,
                          sat_tx_antenna,
                          gs_receiver,
                          ka_channel,
                          rx_interconnect,
                          tx_interconnect,
                          modulation,
                          pylink.LinkBudget(name='Ka Downlink',
                                            is_downlink=True)])

UPLINK = pylink.DAGModel([geometry,
                      sat_rx_antenna,
                      sat_receiver,
                      gs_transmitter,
                      gs_tx_antenna,
                      ka_channel,
                      pylink.LinkBudget(name='Ka Uplink',
                                        is_downlink=False)])
