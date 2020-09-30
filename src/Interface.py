# Yuxuan Cheng
# Interface
import os
from os import listdir
from os.path import isfile, join
from FileReader import Reader, NewData, OldData
from Processor import Processor
from Plotter import PlotCircle



if __name__ == "__main__":

    # get file paths
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    mypath = "../data"
    onlyfiles = [join(mypath, f) for f in listdir(mypath) if isfile(join(mypath, f))]

    # processing data
    processor = Processor(onlyfiles, NewData)
    processor.cal_angles()
    concave_list = processor.pick_concave()
    plotter = PlotCircle(concave_list)
    

