import numpy as np
import matplotlib.pyplot as plt
import math
import random


def GetSecusers(nums, BS_locations_x, BS_locations_y):
  
  xy_all = np.zeros((3*nums, 2))
  for j in range(7):
    count = 0
    m = 0
    p2 = np.zeros((nums,2)) 
    hk = np.array([BS_locations_x[j],BS_locations_y[j]])

    while(count<3):
      a = np.array([X[j, 0+m] - BS_locations_x[j], Y[j, 0+m] - BS_locations_y[j]])
      b = np.array([X[j, 2+m] - BS_locations_x[j], Y[j, 2+m] - BS_locations_y[j]])
      p = []
      for i in range(nums):
        u1 = np.random.uniform(0,1)                
        u2 = np.random.uniform(0,1)  
        p.append(u1*a + u2*b)
      p = np.array(p+hk)
      angle_cord= p - hk
      angles = np.arctan2(angle_cord[:,1], angle_cord[:,0])  #np.arctan2(y, x)


      if(count==0):
        p2 = p
        angles2 = angles
      else:
        p2 = np.concatenate((p2, p),axis=0)
        angles2 = np.concatenate((angles2, angles),axis=0)
      m+=2
      count+=1

    #CLUB ALL Base station users
    if(j==0):
      xy_all = p2
      angles_all = angles2
    else:
      xy_all = np.concatenate((xy_all, p2), axis=0)
      angles_all = np.concatenate((angles_all, angles2),axis=0)  

  n_users, nu = np.shape(xy_all)
  #print(np.shape(xy_all))
  #print(n_users)

  return n_users, xy_all[:,0], xy_all[:,1]
    