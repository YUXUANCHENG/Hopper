# Yuxuan Cheng
# Plotter class

import matplotlib.pyplot as plt
import numpy as np
import math
#import seaborn as sns

class BasePlot:
    def show_plot(self):
        raise NotImplementedError 


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

class AngleDistribution(BasePlot):
    def __init__(self, data_set):
        if len(data_set) == 0:
            raise ValueError("empty circle list!")
        for key in data_set:
            plt.title('Width: {}'.format(key), fontsize=18)
            self.show_plot(data_set[key])

    def show_plot(self, data):
        data = [x/math.pi*180 for x in data]
        plt.hist(x = data, bins = 15, rwidth = 0.9, density =True)
        plt.xlabel('Angle', fontsize=18)
        plt.ylabel('Density', fontsize=18)
        plt.xlim([80, 180])
        plt.show()

class AngleDistribution_shaded(BasePlot):
    def __init__(self, data_set):
        if len(data_set) == 0:
            raise ValueError("empty circle list!")
        self.show_plot(data_set)

    def show_plot(self, data_set):
        for key in data_set:
            data = [x/math.pi*180 for x in data_set[key]]
            sns.distplot(x = data, hist = False, kde = True,
                 kde_kws = {'shade': True, 'linewidth': 3},
                 label = key)
        plt.xlabel('Angle', fontsize=18)
        plt.ylabel('Density', fontsize=18)
        plt.xlim([80, 180])
        plt.show()

