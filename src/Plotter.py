# Yuxuan Cheng
# Plotter class

import matplotlib.pyplot as plt
import numpy as np
import math
import seaborn as sns

class BasePlot:
    def add_title(self,title):
        raise NotImplementedError 
    def show_plot(self):
        raise NotImplementedError 
    def add_data(self, data):
        raise NotImplementedError 

class AngleDistribution(BasePlot):
    def __init__(self, data_set):
        if len(data_set) == 0:
            raise ValueError("empty circle list!")
        for key in data_set:
            self.add_title(key) 
            self.add_data(data_set[key])
            self.show_plot()

    def add_title(self, title):
        plt.title('Width: {}'.format(title), fontsize=18)

    def add_data(self, data):
        data = [x/math.pi*180 for x in data]
        plt.hist(x = data, bins = 15, rwidth = 0.9, density =True)   

    def show_plot(self):
        plt.xlabel('Angle', fontsize=18)
        plt.ylabel('Density', fontsize=18)
        plt.xlim([80, 180])
        plt.show()

class AngleDistribution_shaded(AngleDistribution):
    def __init__(self, data_set):
        if len(data_set) == 0:
            raise ValueError("empty data set!")
        for key in data_set:
            self.add_data(data_set[key], key)
        self.show_plot()

    def add_data(self, data, key):
        data = [x/math.pi*180 for x in data]
        sns.distplot(data, hist = False, kde = True,
                kde_kws = {'shade': True, 'linewidth': 3},
                label = key)
        plt.legend()
        


class NDistribution(AngleDistribution):
    def add_data(self, data):
        plt.hist(x = data, rwidth = 0.9, density =True, bins = [2, 3, 4, 5])

    def show_plot(self):
        plt.xlabel('N', fontsize=18)
        plt.ylabel('Density', fontsize=18)
        plt.show()

class AngleDistributionVSN(AngleDistribution):

    def add_title(self, title):
        plt.title('N: {}'.format(title), fontsize=18)

    def add_data(self, data):
        data = [x/math.pi*180 for x in data]
        plt.hist(x = data, bins = 10, rwidth = 0.9, density =True)

class AngleDistributionVSN_shaded(AngleDistribution_shaded):
    pass

class AngleGravityN_shaded(AngleDistribution_shaded):
    def add_data(self, data, key):
        if key[0] == 3 and len(data) > 10:
            data = [x/math.pi*180 for x in data]
            sns.distplot(data, hist = False, kde = True,
                    kde_kws = {'shade': True, 'linewidth': 3},
                    #label = "N: {}, g: {}".format(key[0], key[1]))
                    label = "g: {}".format(key[1]))
        plt.legend()



class PlotCircle(BasePlot):
    def __init__(self, positions):
        if len(positions) == 0:
            raise ValueError("empty circle list!")
        for position in positions:
            self.circles = []
            self.ax = []
            self.create_circle(position)
            self.add_line(position)
            self.show_plot()

    def create_circle(self, positions):
        for (x, y, r) in np.reshape(positions,(-1,3)):
            self.circles.append(plt.Circle((x, y), radius= r))
        
    def add_line(self, positions):
        pos_temp = np.reshape(positions,(-1,3))
        plt.plot(pos_temp[:,0], pos_temp[:,1], 'r')
        

    def show_plot(self):
        self.ax=plt.gca()
        for patch in self.circles:
            self.ax.add_patch(patch)
        plt.axis('scaled')
        plt.show()