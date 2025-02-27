# -*- coding: utf-8 -*-
"""
Module to transform an ensemble of cumulative data, e.g. cumulative streamflow 
time series, into instantaneous.

To speed-up the computation this module applies the just-in-time compiler Numba
(http://numba.pydata.org/; Lam & Seibert, 2015) .

This module is part of the iRONS toolbox by A. Peñuela and F. Pianosi and at 
Bristol University (2020).

Licence: MIT

References:
Lam, P., Siu Kwan, & Seibert, S. (2015). Numba: A llvm-based python jit 
compiler. doi:10.1145/2833157.2833162
"""

import numpy as np
import numba

@numba.jit(nopython=True) # to speed-up the function
def cum2inst(cum_data):
    """
    This modules uses two for loops to transform element by element of the 
    cumulative data contained in the cum_data array into instantaneous. For 
    every time-step and every ensemble member
    """
    inst_data = np.zeros(cum_data.shape)
    for j in np.arange(len(cum_data[0,:])): # j = column number (ensemble member)
        for i in np.arange(len(cum_data[:,0])-1): # i = row number (time-step)
            inst_data[i+1,j] = np.maximum(cum_data[i+1,j]-cum_data[i,j],0)
    inst_data[0,:] = cum_data[0,:]

    return inst_data
    