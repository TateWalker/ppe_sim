#!/usr/bin/env python

import os
import pylink
import shutil
import numpy as numpy
import subprocess


if __name__ == '__main__':

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

  gs_transmitter = pylink.Transmitter(tx_power_at_pa_dbw=23,
                                      name='Ground Ka-Band Transmitter')

  sat_transmitter = pylink.Transmitter(tx_power_at_pa_dbw=1.5,
                                       name='Satellite Ka-Band Transmitter')

  rx_interconnect = pylink.Interconnect(is_rx=True)


  tx_interconnect = pylink.Interconnect(is_rx=False)


  x_channel = pylink.Channel(bitrate_hz=1e6,
                             allocation_hz=500e4,
                             center_freq_mhz=8200,
                             atmospheric_loss_db=1,
                             ionospheric_loss_db=1,
                             rain_loss_db=2,
                             multipath_fading_db=0,
                             polarization_mismatch_loss_db=3)

    DOWNLINK = pylink.DAGModel([geometry,
                              gs_rx_antenna,
                              sat_transmitter,
                              sat_tx_antenna,
                              gs_receiver,
                              x_channel,
                              rx_interconnect,
                              tx_interconnect,
                              modulation,
                              pylink.LinkBudget(name='Example XBand Downlink',
                                                is_downlink=True)])

  
    # We use 'm' here because it is fewer characters than 'model' and
    # I'm lazy.
    m = eg_budgets.DOWNLINK

    # The same here with 'e' instead of 'enum'...'e' also doesn't
    # collide with the 'enum' package name.
    e = m.enum

    # First, we create the report object.  Most of the interesting
    # stuff happens in the to_latex method.
    r = pylink.Report(m)

    # This example is designed to place the result in the export directory
    output_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                              'export')
    output_path = os.path.join(output_dir, 'interference_analysis.tex')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # We use a LaTeX import directive to include a complicated
    # introduction tex document, so we want to make sure we copy it
    # into the output directoy so that pdflatex will pick it up.
    shutil.copy('intro.tex', output_dir)
        
    # ITU-R SF.358-5 Lays out the maximum permissible PFD values for
    # various bands.
    limits=[(0, -150),
            (5, -150),
            (25, -140),
            (90, -140)]

    # The Canonical PFD figure is the 4kHz BW (though that is tunable
    # if you so desire) peak PFD at the Earth's surface (ie max xmit
    # power, peak antenna gain) as a function of elevation angle,
    # ignoring things like rain fade, since this figure is mostly
    # useful for compliance.
    title = 'Peak PFD at Surface (4kHz BW)'
    canonical_pfd = pylink.CanonicalPFDFigure(m,
                                              title=title,
                                              pfd_limits=limits)

    # Expected PFD is more complicated, as it assumes normal satellite
    # operations (ie Nadir pointing for example), and real antenna
    # patterns instead of peak gain, etc.
    title = 'Expected PFD at Surface (4kHz BW)'
    expected_pfd = pylink.ExpectedPFDFigure(m,
                                            title=title,
                                            pfd_limits=limits)

    # In some cases, it can be useful to produce graphs of peak PFD vs
    # bandwidth to show compliance with various limits.  That's where
    # this class comes in handy.
    title = 'Peak PFD vs Bandwidth at Potential Victim GS'
    rx_bw_pfd = pylink.PFDvsBWFigure(m,
                                     start_hz=1e3,
                                     end_hz=5e3,
                                     is_gso=False,
                                     pfd_limits=None,
                                     title=title)
    title = 'Peak PFD vs Bandwidth at Potential Victim GSO'
    gso_bw_pfd = pylink.PFDvsBWFigure(m,
                                      start_hz=1e3,
                                      end_hz=5e3,
                                      is_gso=True,
                                      pfd_limits=None,
                                      title=title)

    # To make things clear to the regulators for whom this report is
    # being prepared, we're going to want to call out, specifically,
    # the PFD limit, as well as the max potential interference we
    # could cause.
    #
    # And before you say it, I know, the format for these added
    # sections aren't terribly clean...I'll add a ticket to clean this
    # up at some point.  In the meantime, you have a working example
    # below.
    elevation = m.min_elevation_deg
    m.override(e.min_elevation_deg, 90)
    peak_pf = m.peak_pfd_dbw_per_m2_per_hz
    m.override(e.min_elevation_deg, elevation)
    extra_interference_sections = [
        ('Hey Regulators, Look In this Section',
         [('Lowest Permissible PFD (4kHz BW) at Receiver',
           -150,
           'dBW/m^2'),
          ('Peak Possible PFD (4kHz BW) at Receiver',
           peak_pf + pylink.to_db(4e3),
           'dBW/m^2'),
             ])]

    # It may also be worth adding a couple of other random sections to
    # call out something necessary to the business case, or some other
    # computation.  Note the way we escape the ampersand in the title
    # below.  That's because, at the end of the day, a LaTeX file is
    # generated, and & is a reserved character.
    sub_ttc = (
        'Bitrate Requirements for TT\\&C',
         [
            ('Number of Log Files',   1000, ''),
            ('Size of Each Log File', 16, 'kB'),
            ('Minimum Average Bitrate', 9600, 'kbps'),
            ]
        )
    sub_images = (
        'Bitrate Requirements for Images',
         [
            ('Number of Images',   1000, ''),
            ('Size of Each Image', 32, 'MB'),
            ('Minimum Average Bitrate', 32, 'mbps'),
            ]
        )
    extra_regular_sections = [('Bitrates (Custom Section Example)',
                               [sub_ttc,
                                sub_images]),]


    # Now that we've lined everything up, it's time to build some LaTeX
    r.to_latex(output_path,
               author='Harrison Caudill',
               intro='\\input{intro}',
               expo='So long, and thanks for all the Fish!',
               rx_pfd_bws=[1e3, 4e3, 1e6],
               gso_pfd_bws=[1e3, 4e3, 1e6],
               watermark_text='Example',
               pfd_figures=[canonical_pfd,
                            expected_pfd,
                            rx_bw_pfd,
                            gso_bw_pfd],
               bitrate_figure=pylink.BitrateFigure(m, 'Max Bitrate'),
               added_sections=extra_regular_sections,
               added_interference_sections=extra_interference_sections,)
