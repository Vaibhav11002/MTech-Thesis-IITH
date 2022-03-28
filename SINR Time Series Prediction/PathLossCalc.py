import numpy as np
import matplotlib.pyplot as plt
import math
import random

def getdist(n_users,x,y, time_instants):
  h_bs = 25 #m
  h_ut = 1.5 #m
  h = 5 #avg building height
  h_act = h_bs - h_ut #m

  #distance from each user to base station
  Dr_2d = np.zeros((time_instants, 7*7*3, n_users))

  for t in range(time_instants):
    for i in range(7*7*3):
      for j in range(n_users):
        Dr_2d[t][i][j] = math.sqrt(pow(BS_wrap_around_total3x[i] - x[t][j], 2) + pow(BS_wrap_around_total3y[i] - y[t][j], 2)) 

  Dr_3d = np.zeros((time_instants, 7*7*3, n_users))

  for t in range(time_instants):
    for i in range(7*7*3):
      for j in range(n_users):
        Dr_3d[t][i][j] = math.sqrt(pow(Dr_2d[t][i][j], 2) + pow(h_act, 2))

  return Dr_2d, Dr_3d


#PL model for RMA scenario

def PathlossRMA(d_2d, d_3d):
  f_c = 2.3 #GHz
  c = 3*pow(10,8) #m/s

  h_ut = 1.5 #m
  h_bs = 35 #m
  h = 5 #m --avg. building height
  W = 20 #m --avg. street width

  d_bp = 2*math.pi*h_bs*h_ut*f_c*pow(10,9)/c

  #LOS probability
  if d_2d <= 10:
    P_los = 1
  else:
    P_los = math.exp(-1*(d_2d-10)/1000)
    
  PL_1 = 20*math.log(40*math.pi*d_3d*f_c/3 , 10) + min(0.03*pow(h, 1.72) , 10)*math.log(d_3d, 10) - min(0.044*pow(h, 1.72) , 14.77) + 0.002*math.log10(h)*d_3d
  PL_2 = PL_1*d_bp + 40*math.log10(d_3d/d_bp)

  #NLOS
  #PL_NLOS = 161.04 - 7.1*math.log10(W) +7.5*math.log10(h) - (24.37-3.7*pow(h/h_bs, 2))*math.log10(h_bs) + (43.42-3.1*math.log10(h_bs))*(math.log10(d_3d)-3) + 20*math.log10(f_c) - (3.2*pow(math.log10(11.75*h_ut) , 2) - 4.97)
  PL_NLOS = 0

  #LOS for prob>0.5
  if P_los >= 0.5:
    if d_2d <= d_bp:
      return PL_1
    elif d_2d > d_bp and d_2d < 10*1000:
      return PL_2

  else: #NLOS for prob<0.5
    if d_2d <= d_bp:
      return max(PL_1, PL_NLOS)
    elif d_2d > d_bp and d_2d < 5000:
      return max(PL_2, PL_NLOS)

#PL model for UMA scenario

def PathlossUMA(d_2d, d_3d):
  f_c = 2.3 #GHz
  c = 3*pow(10,8) #m/s
  h_ut = 1.5 #m
  h_bs = 25 #m
  h_e = 1
  h_bs_eff = h_bs - h_e
  h_ut_eff = h_ut - h_e

  d_bp_eff = 4*h_bs_eff*h_ut_eff*f_c*pow(10,9)/c

  #LOS probability
  #for outdoor users
  if d_2d <= 18:
    P_los = 1
  else:
    if h_ut <= 13:
      C_h = 0
    else:
      C_h = pow((h_ut - 13)/10, 1.5)
    
    temp1 = (math.exp(-1*d_2d/63))*(1 - 18/d_2d)
    #temp2 = 1 + C_h*(5/4)*pow(d_2d/100, 3)*math.exp(-d_2d/150)
    temp2 = 1
    P_los = (18/d_2d + temp1)*temp2
    #print(P_los)

  #print(P_los)
  PL_1 = 28 + 22*math.log(d_3d, 10) + 20*math.log(f_c, 10)
  PL_2 = 28 + 40*math.log(d_3d, 10) + 20*math.log(f_c, 10) - 9*math.log(pow(d_bp_eff, 2) + pow(h_bs - h_ut, 2) , 10)
  #PL_NLOS = 13.54 + 39.08*math.log(d_3d, 10) + 20*math.log(f_c, 10) - 0.6*(h_ut - 1.5)
  PL_NLOS = 0

  #LOS for prob>0.5
  if P_los >= 0.5:
    if d_2d <= d_bp_eff:
      return PL_1
    elif d_2d > d_bp_eff and d_2d < 5000:
      return PL_2

  else: #NLOS for prob<0.5
    if d_2d <= d_bp_eff:
      return max(PL_1, PL_NLOS)
    elif d_2d > d_bp_eff and d_2d < 5000:
      return max(PL_2, PL_NLOS)


def PathLoss(dist2d, dist3d, n_users):
  Dr_2d, Dr_3d = dist2d, dist3d
  
  PLr = np.zeros(np.shape(Dr_2d))

  time_instants, row, col = np.shape(Dr_2d)

  #path loss calculation
  for t in range(time_instants):
    for i in range(7*7*3):
      for j in range(n_users):
        #PLr[t][i][j] = PathlossRMA(Dr_2d[t][i][j], Dr_3d[t][i][j])   #for RMA
        PLr[t][i][j] = PathlossUMA(Dr_2d[t][i][j], Dr_3d[t][i][j])   #for UMA
  
  return PLr
