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

    def combine_angle_with_width(self):
        if len(self.angles) != len(self.width):
            raise ValueError("Dimensions don't agree!")
        data_set = {}
        for index, angle in enumerate(self.angles):
            if angle:
                width = self.width[index]
                if width in data_set:
                    data_set[width] += angle
                else:
                    data_set[width] = angle
        return data_set

    def combine_N_with_width(self):
        if len(self.N) != len(self.width):
            raise ValueError("Dimensions don't agree!")
        data_set = {}
        for index, N in enumerate(self.N):
            width = self.width[index]
            if width in data_set:
                data_set[width].append(N)
            else:
                data_set[width] = [N]
        return data_set

    def combine_angle_with_N(self):
        if len(self.N) != len(self.angles):
            raise ValueError("Dimensions don't agree!")
        data_set = {}
        for index, angle in enumerate(self.angles):
            if angle:
                N = self.N[index]
                if N in data_set:
                    data_set[N] += angle
                else:
                    data_set[N] = angle
        return data_set

    def combine_angle_with_N_and_g(self):
        if len(self.gravity) != len(self.angles):
            raise ValueError("Dimensions don't agree!")
        data_set = {}
        for index, angle in enumerate(self.angles):
            if angle:
                N = self.N[index]
                g = self.gravity[index]
                if (N, g) in data_set:
                    data_set[(N, g)] += angle
                else:
                    data_set[(N, g)] = angle
        return data_set

    def deviation_of_angles(self):
        pass






