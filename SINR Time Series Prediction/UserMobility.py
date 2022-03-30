import numpy as np
import matplotlib.pyplot as plt
import math
import random

#Random Waypoint Model
def User_Mobility(radius, total_user, xs, ys, v_min, v_max, Time_instants):
  isd = 0.5*math.sqrt(3)*radius
  # range of x and y coordinates for user mobility
  x_min = -2.25*radius
  x_max = 2.25*radius

  y_min = -1.5*isd
  y_max = 1.5*isd


  # position matrices
  x_pos = np.zeros((total_user, Time_instants))
  y_pos = np.zeros((total_user, Time_instants))

  

  # Choose velocity uniformly between v_min and v_max
  velocity = np.random.randint(v_min, v_max, (total_user))#, Time_instants)) #m/sec  #total_users x Time_instants
  #print(np.shape(velocity))

  for i in range(total_user):

    x_previous = xs[i]
    y_previous = ys[i]



    # User starts from initial position to a final position
    x_pos[i,0] = xs[i]
    y_pos[i,0] = ys[i]


    for t in range(1,Time_instants):

      #directions of the mobile users
      theta = np.random.randint(0,360)

      x_pos[i,t] = x_previous + velocity[i]* math.cos(math.radians(theta))

      if x_pos[i,t]>x_max or x_pos[i,t]<x_min:
        theta = 180 - theta
        x_pos[i,t] = x_previous + velocity[i]* math.cos(math.radians(theta))

      y_pos[i,t] = y_previous + velocity[i]* math.sin(math.radians(theta))

      if y_pos[i,t]>y_max or y_pos[i,t]<y_min:
        theta = 180 - theta
        y_pos[i,t] = y_previous + velocity[i]* math.sin(math.radians(theta))

      # Now the current position of the users becomes the previous position for next time instant
      x_previous = x_pos[i,t]
      y_previous = y_pos[i,t]


  x_mobile = np.transpose(x_pos) #time_instants x total_users
  y_mobile = np.transpose(y_pos)

  velocity_users = np.transpose(velocity)
  
  return x_mobile, y_mobile, velocity_users
