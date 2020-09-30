# Yuxuan Cheng
# Interface class
import numpy as np
import os
from os import listdir
from os.path import isfile, join
from FileReader import Reader, NewData, OldData

class Processor(Reader):
    def __init__(self, file_list, data_type):
        super().__init__(file_list)
        self.data_type = data_type
        self.data_processor = self.data_type(self.content)
        self.data_processor.check_dimension()
        self.angles = []

    def test(self):
        print(np.mean(self.data_processor.N))

    def cal_angles(self):
        position = []
        for positions in self.data_processor.position:
            position = []
            angles = []
            for (x, y, r) in np.reshape(positions,(-1,3)):
                position.append([x, y])
            position = np.array(position)
            iter1 = iter(position)
            iter2 = iter(position)
            next(iter2)
            vectors = []
            for pos in iter2:
                vectors.append(pos - next(iter1))
            iter1 = iter(vectors)
            iter2 = iter(vectors)
            next(iter2)
            for vector in iter2:
                angles.append(Processor.angle_between(next(iter1), vector))
            self.angles.append(angles)

    @staticmethod
    def unit_vector(vector):
        return vector / np.linalg.norm(vector)

    @staticmethod
    def angle_between(v1, v2):
        v1_u = Processor.unit_vector(v1)
        v2_u = Processor.unit_vector(v2)
        return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))



if __name__ == "__main__":
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    mypath = "../data"
    onlyfiles = [join(mypath, f) for f in listdir(mypath) if isfile(join(mypath, f))]
    processor = Processor(onlyfiles, NewData)
    processor.cal_angles()
    print(len(processor.angles))
    

