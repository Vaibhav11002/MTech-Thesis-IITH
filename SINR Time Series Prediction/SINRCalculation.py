import numpy as np
import matplotlib.pyplot as plt
import math
import random

def SINR_b4(channel_gain_matrix, BS_locations_x, BS_locations_y, BS_wrap_around_total3x, BS_wrap_around_total3y):
  #e total transmit power of a BS, Ps = 46dBm
  #dBm to watts
  #Ps = 46dBm--->39.81071706W ---> 10log(39.81071706) = 16dB
  M = 99

  Ps_dbm = 46 #dbm
  
  #dBm TO watts CONVERTER
  Ps_lin = pow(10, (Ps_dbm-30)/10)   #Psdbm is in dBm and Ps_watt in Watts
  Ps_lin = Ps_lin/M

  #watts TO dB CONVERTER
  Ps_dB = 10*math.log10(Ps_lin) #dB

  #calculation in linear then converting to dB
  signal_power_matrix = Ps_lin * channel_gain_matrix[:,0:21, :]


  #NOISE
#------------------------------------------------------------------------------------
  #noise power kTB, kT = -174dBm/Hz, BW = bandwidth       
  #kTB(dBm) = -174 + 10log(BW) 
#------------------------------------------------------------------------------------
  
  noise = -174 + 10*math.log10(180*1000) #dBm         BW = 180KHz                   
  #dBm TO watts CONVERTER
  noise_watt = pow(10, (noise-30)/10)   #noise is in dBm and noise_watt in Watts
  #watts TO dB CONVERTER
  noise_dB = 10*math.log(noise_watt, 10) #dB


  #INTERFERENCE
  interference_matrix = np.zeros(np.shape(channel_gain_matrix[:,0:21, :]))

  intf_time, intf_bs, intf_user = np.shape(interference_matrix)

  total_time, total_base_stations, total_users = np.shape(channel_gain_matrix)

  bs_reference = []

  in_one_cell = total_users#int(total_users/7) #total users in one hex cell

  for k in range(7):
    for i in range(in_one_cell):
      bs_reference.append(k)
  
  bs_reference = np.array(bs_reference)

  #print(np.shape(bs_reference))


  for inft in range(intf_time):
    for bss in range(intf_bs):
      for user in range(intf_user): 
        m = bs_reference[user]
        x_dis = BS_locations_x[m]
        y_dis = BS_locations_y[m]
        for j in range(total_base_stations):
          interference_distance = math.sqrt(pow(x_dis - BS_wrap_around_total3x[j], 2) + pow(y_dis - BS_wrap_around_total3y[j], 2))
          if (j!=bss and  math.floor(interference_distance) <= ISD):
            interference_matrix[inft][bss][user] +=  Ps_lin * channel_gain_matrix[inft][j][user]

 
  #SINR
  interference_plus_noise_matrix = 0.33*interference_matrix + noise_watt

  sinr = signal_power_matrix/interference_plus_noise_matrix  #linear

  sinr_dB = 10*np.log10(sinr) #dBe
  sinr_mean = np.mean(sinr_dB)

  return sinr_dB, signal_power_matrix, interference_plus_noise_matrix
