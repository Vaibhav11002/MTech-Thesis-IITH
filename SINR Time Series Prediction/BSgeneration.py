import numpy as np
import matplotlib.pyplot as plt
import math
import random

class BSGenerate:
    def __init__(self, radius):
        self.radius = radius
        self.BS_total_x = None
        self.BS_total_y = None
        self.BS_location_x = None
        self.BS_location_y = None


    def tier1cellgen(self):
        #self.radius = 500

        t = np.linspace(0, 2*math.pi, 7)

        #center cell
        x1 = []
        y1 = []
        for i in range(len(t)):
            x1.append(0 + self.radius*math.cos(t[i]))
            y1.append(0 + self.radius*math.sin(t[i]))

        c_x1 = 0  #BS Location Center Cell x-axis
        c_y1 = 0 #BS Location Center Cell y-axis


        #upper cell
        x2 = []
        y2 = [] 
        for i in range(len(t)):
            x2.append(0+self.radius*math.cos(t[i]))
            y2.append(((math.sqrt(3)/2)*2*self.radius) + (self.radius*math.sin(t[i])))

        c_x2 = 0  #BS Location Upper Cell x-axis
        c_y2 = ((math.sqrt(3)/2)*2*self.radius) #BS Location Upper Cell y-axis


        #lower cell
        x3 = []
        y3 = []
        for i in range(len(t)):
            x3.append(0+self.radius*math.cos(t[i]))
            y3.append(-((math.sqrt(3)/2)*2*self.radius) + (self.radius*math.sin(t[i])))

        c_x3 = 0  #BS Location Lower Cell x-axis
        c_y3 = -((math.sqrt(3)/2)*2*self.radius) #BS Location Lower Cell y-axis


        #right upper cell
        x4 = []
        y4 = []
        for i in range(len(t)):
            x4.append((self.radius+(self.radius/2)) + self.radius*math.cos(t[i]))
            y4.append(((math.sqrt(3)/2)*self.radius) + (self.radius*math.sin(t[i])))

        c_x4 = (self.radius+(self.radius/2))  #BS Location right upper Cell x-axis
        c_y4 = ((math.sqrt(3)/2)*self.radius) #BS Location right upper Cell y-axis


        #%Right Lower cell
        x5 = []
        y5 = []
        for i in range(len(t)):
            x5.append((self.radius+(self.radius/2)) + self.radius*math.cos(t[i]))
            y5.append(-((math.sqrt(3)/2)*self.radius) + (self.radius*math.sin(t[i])))

        c_x5 = (self.radius+(self.radius/2))  #BS Location right lower Cell x-axis
        c_y5 = -((math.sqrt(3)/2)*self.radius) #BS Location right lower Cell y-axis


        #%Left Upper cell
        x6 = []
        y6 = []
        for i in range(len(t)):
            x6.append(-(self.radius+(self.radius/2)) + self.radius*math.cos(t[i]))
            y6.append(((math.sqrt(3)/2)*self.radius) + (self.radius*math.sin(t[i])))

        c_x6 = -(self.radius+(self.radius/2))  #BS Location Left upper x-axis
        c_y6 = ((math.sqrt(3)/2)*self.radius) #BS Location Left upper y-axis


        #left lower cell
        x7 = []
        y7 = []
        for i in range(len(t)):
            x7.append(-(self.radius+(self.radius/2)) + self.radius*math.cos(t[i]))
            y7.append(-((math.sqrt(3)/2)*self.radius) + (self.radius*math.sin(t[i])))

        c_x7 = -(self.radius+(self.radius/2)) #BS Location left lower Cell x-axis
        c_y7 = -((math.sqrt(3)/2)*self.radius) #BS Location left lower Cell y-axis


        self.BS_location_x = [c_x1, c_x2, c_x3, c_x4, c_x5, c_x6, c_x7]    #centre, up, low, right up, right low, left up, left low
        self.BS_location_y = [c_y1, c_y2, c_y3, c_y4, c_y5, c_y6, c_y7]
        print(self.BS_location_y)

        X =np.array([x1,x2,x3,x4,x5,x6,x7])
        Y =np.array([y1,y2,y3,y4,y5,y6,y7])




        diff = [c_x4, c_y4] 
        ISD = np.linalg.norm(diff)
        #print("ISD: ", ISD)

        # 2nd cell
        isd = math.sqrt(3)*self.radius
        BS2x = [x + (-3*self.radius) for x in self.BS_location_x]
        BS2y = [y + (2*isd) for y in self.BS_location_y]

        #3rd
        BS3x = [x + (1.5*self.radius) for x in self.BS_location_x]
        BS3y = [y + (2.5*isd) for y in self.BS_location_y]

        #4th
        BS4x = [x + (4.5*self.radius) for x in self.BS_location_x]
        BS4y = [y + (0.5*isd) for y in self.BS_location_y]

        #5th
        BS5x = [x + (3*self.radius) for x in self.BS_location_x]
        BS5y = [y + (-2*isd) for y in self.BS_location_y]

        #6th
        BS6x = [x + (-1.5*self.radius) for x in self.BS_location_x]
        BS6y = [y + (-2.5*isd) for y in self.BS_location_y]

        #7th
        BS7x = [x + (-4.5*self.radius) for x in self.BS_location_x]
        BS7y = [y + (-0.5*isd) for y in self.BS_location_y]

        self.BS_total_x = [self.BS_location_x, BS2x, BS3x, BS4x, BS5x, BS6x, BS7x]
        self.BS_total_y = [self.BS_location_y, BS2y, BS3y, BS4y, BS5y, BS6y, BS7y]


        return X, Y


    def WrapAround(self):

        BS_wrap_around_x = sum(self.BS_total_x, [])
        BS_wrap_around_y = sum(self.BS_total_y, [])

        BS_wrap_around_total3x = []
        for i in BS_wrap_around_x:
            for j in range(3):
                BS_wrap_around_total3x.append(i)

        BS_wrap_around_total3y = []
        for i in BS_wrap_around_y:
            for j in range(3):
                BS_wrap_around_total3y.append(i)

        BS_cor_x = np.array(BS_wrap_around_total3x)
        BS_cor_y = np.array(BS_wrap_around_total3y)

        return BS_wrap_around_total3x, BS_wrap_around_total3y

    
