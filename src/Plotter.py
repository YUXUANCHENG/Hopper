# Yuxuan Cheng
# Plotter class

import matplotlib.pyplot as plt
import numpy as np

class BasePlot:
    def show_shape(patch):
        raise NotImplementedError 


class PlotCircle(BasePlot):
    def __init__(self, positions):
        self.circles = []
        self.ax = []
        try:
            self.create_circle(positions)
            self.add_line(positions)
            self.show_shapes()
        except ValueError as e:
            print(e)

    def create_circle(self, positions):
        if len(positions) == 0:
            raise ValueError("empty circle list!")
        for (x, y, r) in np.reshape(positions,(-1,3)):
            self.circles.append(plt.Circle((x, y), radius= r))
        
    def add_line(self, positions):
        pos_temp = np.reshape(positions,(-1,3))
        plt.plot(pos_temp[:,0], pos_temp[:,1], 'r')
        

    def show_shapes(self):
        self.ax=plt.gca()
        for patch in self.circles:
            self.ax.add_patch(patch)
        plt.axis('scaled')
        plt.show()

