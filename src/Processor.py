# Yuxuan Cheng
# data processor class
import numpy as np
import math
from abc import ABCMeta, abstractproperty

class Processor(metaclass=ABCMeta):
    def __init__(self, file_list):
        self.angles = []

    #@abstractproperty
    #def position():
    #    pass

    def cal_angles(self):
        for positions in self.position:
            position = []
            angles = []
            if len(positions) > 2 * 3:
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
                concave.append(self.position[index])
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

    def __combine_parameters(self, arg1, *args):
        for key in args:
            if len(arg1) != len(key):
                raise ValueError("Dimensions don't agree!")
        data_set = {}
        for index, data1 in enumerate(arg1):
            if data1:
                if len(args) == 1:
                    keys = args[0][index]
                else:
                    keys = []
                    for key in args:
                        keys.append(key[index])
                    keys = tuple(keys)
                if keys in data_set:
                    if type(data1) is list:
                        data_set[keys] += data1
                    else:
                        data_set[keys].append(data1)
                else:
                    if type(data1) is list:
                        data_set[keys] = data1
                    else:
                        data_set[keys] = [data1]
        return data_set

    def combine_angle_with_width(self):
        return self.__combine_parameters(self.angles, self.width)

    def combine_N_with_width(self):
        return self.__combine_parameters(self.N, self.width)

    def combine_angle_with_N(self):
        return self.__combine_parameters(self.angles, self.N)

    def combine_angle_with_N_and_g(self):
        return self.__combine_parameters(self.angles, self.N, self.gravity)

    def deviation_of_angles(self):
        pass






