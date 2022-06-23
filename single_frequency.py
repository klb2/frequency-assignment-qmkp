import logging

import numpy as np
from scipy import constants

from util import to_decibel

from model import length_los, length_ref


LOGGER = logging.getLogger(__name__)


def rec_power(distance, freq, h_tx, h_rx, G_los=1, G_ref=1, c=constants.c,
              power_tx=1):
    d_los = length_los(distance, h_tx, h_rx)
    d_ref = length_ref(distance, h_tx, h_rx)
    omega = 2*np.pi*freq
    phi = omega/c*(d_ref-d_los)
    _factor = power_tx*(c/(2*omega))**2
    _part1 = G_los/(d_los**2)
    _part2 = G_ref/(d_ref**2)
    _part3 = -2*np.sqrt(G_los*G_ref)/(d_los*d_ref) * np.cos(phi)
    power_rx = _factor*(_part1+_part2+_part3)
    return power_rx

def crit_dist(freq, h_tx, h_rx, c=constants.c, k=None):
    a = h_tx - h_rx
    b = h_tx + h_rx
    max_phi = 2*np.pi*freq/c*(b-a)
    max_k = np.divmod(max_phi, 2*np.pi)[0]
    if k is not None:
        if k > max_k: raise ValueError(f"Your provided k is too large. The maximum k is {max_k:d}")
        k = k + 0j
    else:
        k = np.arange(max_k)+1 + 0j
    _d = -1/(2*c*freq*k)*np.sqrt(c**2*k**2 - 4*freq**2*h_rx**2)*np.sqrt(c**2*k**2 - 4*freq**2*h_tx**2)
    _d = np.real(_d)
    return _d

def min_rec_power_single_freq(d_min: float, d_max: float, freq,
                              h_tx, h_rx, c=constants.c):
    _crit_dist = crit_dist(freq, h_tx, h_rx)
    idx_dk_range = np.where(np.logical_and(_crit_dist>=d_min, _crit_dist<=d_max))
    crit_dist_range = _crit_dist[idx_dk_range]
    if len(crit_dist_range) > 0:
        dk_worst = np.max(crit_dist_range)
        _pow_dk = rec_power(dk_worst, freq, h_tx, h_rx)
    else:
        _pow_dk = np.inf
    _pow_dmin = rec_power(d_min, freq, h_tx, h_rx)
    _pow_dmax = rec_power(d_max, freq, h_tx, h_rx)
    return np.min([_pow_dmin, _pow_dk, _pow_dmax])
