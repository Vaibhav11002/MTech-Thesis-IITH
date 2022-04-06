import numpy as np
import matplotlib.pyplot as plt
import math
import random

#angle made by user wrt each base station
def UserAngle(mobileuser_x, mobileuser_y, BS_totalx, BS_totaly):
  
  t, user_num = np.shape(mobileuser_x) #time_instant, total_users

  total_bss = len(BS_totalx)

  all_angles = np.zeros((t, total_bss, user_num))
  dx = np.zeros((t, total_bss, user_num))
  dy = np.zeros((t, total_bss, user_num)) 

  for time in range(t):
    for bs in range(total_bss):
      dx[time][bs] = mobileuser_x[time] - BS_totalx[bs]

  for time in range(t):
    for bs in range(total_bss):
      dy[time][bs] = mobileuser_y[time] - BS_totaly[bs]

  
  all_angles = np.arctan2(dy, dx)  #time_instant x base_station x total_users

  return all_angles

#phi calculation
def FindPhi(user_angles):
  
  user_angles = user_angles*180/math.pi   #radians to degree
  
  t, bs, users = np.shape(user_angles)

  phi = np.zeros((t, bs, users)) #bs = (7*3)*7 = 147 = 49*3

  lobe_angle = np.array([[60,180,-60]*int(bs/3)])
  lobe_angle = lobe_angle.transpose()

  for time in range(t):
    phi[time] = lobe_angle - user_angles[time]


  #phi = lobe_angle - user_angles

  phi = np.where(phi>180, 360-phi, phi)  #convert phi range in -180 to 180 deg i.e., phi = phi>180 ? 360-phi : phi

  return phi*math.pi/180    # degree back to radians


def DirectivityGain(users_phi):
  users_phi = users_phi * 180/math.pi #converts to degree
  dir_gain = 25 - np.minimum(12*np.power(users_phi/70, 2), 20)

  return dir_gain

    