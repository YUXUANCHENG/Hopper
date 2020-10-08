# Yuxuan Cheng
# Interface
import os
import re
from os import listdir
from os.path import isfile, join
from FileReader import NewData, OldData
from Processor import Processor
import Plotter
#AngleDistribution, PlotCircle, AngleDistribution_shaded

class NewInterface(NewData, Processor):
    pass

class OldInterface(OldData, Processor):
    pass

if __name__ == "__main__":

    # get file paths
    # data obtained from http://www.physics.emory.edu/faculty/weeks/data/arches/
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    mypath = "../data"
    oldfiles = [join(mypath, f) for f in listdir(mypath) if isfile(join(mypath, f)) and re.search(r'.*yale\.txt', f)]
    newfiles = [join(mypath, f) for f in listdir(mypath) if isfile(join(mypath, f)) and re.search(r'^sav.*\.txt', f)]
    # processing data
    '''
    old_interface = OldInterface(oldfiles)
    old_interface.cal_angles()
    concave_list = old_interface.pick_concave()
    plotter = Plotter.PlotCircle(concave_list)
    angle_data = old_interface.combine_angle_with_width()
    '''

    new_interface = NewInterface(newfiles)
    new_interface.cal_angles()
    angle_data = new_interface.combine_angle_with_width()
    Plotter.AngleDistribution(angle_data)
    Plotter.AngleDistribution_shaded(angle_data)
    Plotter.NDistribution(new_interface.combine_N_with_width())
    Plotter.AngleDistributionVSN(new_interface.combine_angle_with_N())
    Plotter.AngleDistributionVSN_shaded(new_interface.combine_angle_with_N())
    Plotter.AngleGravityN_shaded(new_interface.combine_angle_with_N_and_g())
    

