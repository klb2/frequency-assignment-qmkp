import logging

import numpy as np
from scipy import constants

from util import to_decibel

from model import length_los, length_ref
from single_frequency import rec_power, crit_dist


LOGGER = logging.getLogger(__name__)


def sum_power_lower_envelope(distance, delta_freq, freq, 
                             h_tx, h_rx, G_los=1, G_ref=1,
                             c=constants.c, power_tx=1):
    d_los = length_los(distance, h_tx, h_rx)
    d_ref = length_ref(distance, h_tx, h_rx)
    freq2 = freq+delta_freq
    omega = 2*np.pi*freq
    omega2 = 2*np.pi*freq2
    delta_omega = omega2-omega
    _part1 = c**2/(4*d_los**2) * (1./omega**2 + 1./omega2**2)
    _part2 = c**2/(4*d_ref**2) * (1./omega**2 + 1./omega2**2)
    A = (c/(2*omega))**2
    B = (c/(2*omega2))**2
    _part3 = -2/(d_los*d_ref) * np.sqrt(A**2 + B**2 + 2*A*B*np.cos(delta_omega/c*(d_ref-d_los)))
    power_rx = power_tx/2 * (_part1 + _part2 + _part3)
    return power_rx

def min_rec_power_two_freq(d_min: float, d_max: float, freq, freq2,
                           h_tx: float, h_rx: float, c=constants.c):
    delta_freq = np.abs(freq2 - freq)
    _crit_dist = crit_dist(delta_freq, h_tx, h_rx)
    idx_dk_range = np.where(np.logical_and(_crit_dist>=d_min, _crit_dist<=d_max))
    crit_dist_range = _crit_dist[idx_dk_range]
    if len(crit_dist_range) > 0:
        dk_worst = np.max(crit_dist_range)
        _pow_dk = sum_power_lower_envelope(dk_worst, delta_freq, freq, h_tx, h_rx)
    else:
        _pow_dk = np.inf
    _pow_dmin = sum_power_lower_envelope(d_min, delta_freq, freq, h_tx, h_rx)
    _pow_dmax = sum_power_lower_envelope(d_max, delta_freq, freq, h_tx, h_rx)
    return np.min([_pow_dmin, _pow_dk, _pow_dmax])
