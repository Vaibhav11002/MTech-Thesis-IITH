import numpy as np
import matplotlib.pyplot as plt
import math
import random

def ChannelGainCalculation(pathloss, shadloss, directivity_gain): #Channel Gain Calculations
    #channel gain dim -> time_steps x base_stations x users
    
    rchgain = - pathloss + directivity_gain - shadloss
    rchgain_lin = np.power(10, (rchgain)/10) #linear

    return rchgain_lin

