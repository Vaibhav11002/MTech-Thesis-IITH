import numpy as np
import matplotlib.pyplot as plt
import math
import random

def correlated_shadowing(x_mobile, y_mobile, sigma_shd, BS_total_x, BS_total_y):
    
    bs_wrap = 49
    D_cor = 100
    #sigma_shd = 100 #dB

    BS_cords = np.concatenate((BS_total_x, BS_total_y), axis=0)
    BS_cords = BS_cords.reshape(2, -1) 

    
    Dist_bs = np.zeros((bs_wrap, bs_wrap))
    Corr_bs = np.zeros(np.shape(Dist_bs))
    
    time_steps, num_users = np.shape(x_mobile)
    
    #shadowing matrix dim -> time_steps x base_stations x total_users
    shadowing_mat = np.zeros((time_steps, 147, num_users))

    for m1 in range(bs_wrap):
        for m2 in range(bs_wrap):
            Dist_bs[m1][m2] = np.linalg.norm(BS_cords[:, m1] - BS_cords[:, m2])
            Corr_bs[m1][m2] = np.exp(-np.log(2)*Dist_bs[m1][m2]/D_cor)

    A1 = np.linalg.cholesky(Corr_bs)
    #print(A1)
    
    bsrandom1 = np.random.normal(size = bs_wrap)

    sh_BS = np.matmul(A1, bsrandom1)
    #print(sh_BS) #dim -> total_base_stations

    for m in range(bs_wrap):
        sh_BS[m] = (1/math.sqrt(2))*sigma_shd*sh_BS[m]/np.linalg.norm(A1[m,:])

    #print(sh_BS)

    # for users
    for time in range(time_steps):
        
        time_steps, num_users = np.shape(x_mobile)
        Dist_user = np.zeros((num_users, num_users))
        Corr_user = np.zeros((num_users, num_users))

        for m1 in range(num_users):
            for m2 in range(num_users):
                Dist_user[m1][m2] = np.linalg.norm([x_mobile[time][m1]-x_mobile[time][m2], y_mobile[time][m1]-y_mobile[time][m2]])
                Corr_user[m1][m2] = np.exp(-np.log(2)*Dist_user[m1][m2]/D_cor)

        A2 = np.linalg.cholesky(Corr_user)
        userrandom1 = np.random.normal(size = num_users)
        
        sh_user = np.matmul(A2, userrandom1) #dim -> num_users

        for m in range(num_users):
            sh_user[m] = (1/math.sqrt(2))*sigma_shd*sh_user[m]/np.linalg.norm(A2[m])
        
        #Shadowing Matrix for each time step:
        
        for bs in range(147):
            for user in range(num_users):
                shadowing_mat[time][bs][user] = sh_BS[bs//3] + sh_user[user]
            
    
    #print(shadowing_mat)

    return shadowing_mat