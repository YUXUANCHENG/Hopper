# Yuxuan Cheng
# Classes for file reader

import numpy as np


class Base:
    '''base class'''
    def __init__(self, file_list):
        self.file_list = file_list
        if len(self.file_list) < 1:
            raise ValueError("empty file list!")
    
    def read(self):
        raise NotImplementedError 

class Reader(Base):
    '''read files'''
    def __init__(self, file_list):
        super().__init__(file_list)
        self.content = np.array([])
        self.read()

    def read(self):
        for file in self.file_list:
            self.content = np.concatenate((self.content, np.loadtxt(file)), axis = 0) if self.content.size else np.loadtxt(file)
        self.content = np.array([row for row in self.content if row[0] != 0])

class NewData:
    '''process new data'''
    def __init__(self, content):
        self.n_trial = len(content)
        self.N = content[:, 0]
        self.N = np.array([int(x) for x in self.N])
        self.position = []
        self._get_position(content)

    def _get_position(self, content):
        for (index, N_particle) in enumerate(self.N):
            position = content[index, 1: 3 * N_particle + 1]
            self.position.append(position)

    def check_dimension(self):
        if (len(self.position) != self.n_trial):
            raise ValueError("content dimensionos don't match")


class OldData(NewData):
    '''process old data'''
    def __init__(self, content):
        super().__init__(content)
        self.gravity = content[:, 49]
        self.n_left = content[:, 46]
        self.width = content[:, 48]
    
    def check_dimension(self):
        super().check_dimension()
        if (len(self.gravity) != self.n_trial or len(self.n_left) != self.n_trial or len(self.width) != self.n_trial):
            raise ValueError("content dimensionos don't match")


