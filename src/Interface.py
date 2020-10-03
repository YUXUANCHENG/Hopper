# Yuxuan Cheng
# Interface
import os
import re
from os import listdir
from os.path import isfile, join
from FileReader import Reader, NewData, OldData
from Processor import Processor
from Plotter import PlotCircle



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
    old_processor = Processor(oldfiles, OldData)
    old_processor.cal_angles()
    concave_list = old_processor.pick_concave()
    plotter = PlotCircle(concave_list)

    new_processor = Processor(newfiles, NewData)
    new_processor.cal_angles()
    

