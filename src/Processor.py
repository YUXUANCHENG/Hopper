# Yuxuan Cheng
# data processor class
import numpy as np
import math
from FileReader import Reader, NewData, OldData

class Processor(Reader):
    def __init__(self, file_list, data_type):
        super().__init__(file_list)
        self.data_type = data_type
        self.data_processor = self.data_type(self.content)
        self.data_processor.check_dimension()
        self.angles = []

    def cal_angles(self):
        for positions in self.data_processor.position:
            position = []
            angles = []
            # get data points
            for (x, y, r) in np.reshape(positions,(-1,3)):
                position.append([x, y])
            position = np.array(position)
            iter1 = iter(position)
            iter2 = iter(position)
            next(iter2)
            vectors = []
            # get vectors based on data points
            for pos in iter2:
                vectors.append(pos - next(iter1))
            iter1 = iter(vectors)
            iter2 = iter(vectors)
            next(iter2)
            # get angles based on vectors
            for vector in iter2:
                vector1 = next(iter1)
                temp = Processor.angle_between(vector1, vector)
                direction = Processor.cal_direction(vector1, vector)
                if direction < 0:
                    angles.append(math.pi - temp)
                else:
                    angles.append(math.pi + temp)
            self.angles.append(angles)

    def pick_concave(self):
        concave = []
        if not self.angles:
            self.cal_angles()
        for (index, angle) in enumerate(self.angles):
            test = [x for x in angle if x > math.pi]
            if test:
                concave.append(self.data_processor.position[index])
        return concave

    @staticmethod
    def unit_vector(vector):
        return vector / np.linalg.norm(vector)

    @staticmethod
    def angle_between(v1, v2):
        v1_u = Processor.unit_vector(v1)
        v2_u = Processor.unit_vector(v2)
        return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

    @staticmethod
    def cal_direction(v1, v2):
        v1 = np.append(v1, 0)
        v2 = np.append(v2, 0)
        return np.cross(v1, v2)[2]

