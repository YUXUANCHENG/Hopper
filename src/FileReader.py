# Yuxuan Cheng
# Classes for file reader
# data obtained from http://www.physics.emory.edu/faculty/weeks/data/arches/


import numpy as np


class Base:
    '''base class'''
    def __init__(self, file_list):
        super().__init__(file_list)
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
        self.file_list = file_list
        self.lines_per_file = []
        self.deleted = []
        self.read()
        

    def read(self):
        for file in self.file_list:
            new_data = np.loadtxt(file)
            if len(new_data) == 0:
                continue
            if self.content.size:
                if self.content.shape[1] == new_data.shape[1]:
                    self.content = np.concatenate((self.content, new_data), axis = 0)
                else:
                    #print("changing format")
                    self.padding(new_data)
            else:
                self.content = new_data 
            self.lines_per_file.append(len(new_data))
        
        # delete configurations with less than 3 partiles
        self.deleted = [row[0] > 0 for row in self.content]
        self.content = np.array([row for row in self.content if row[0] > 0])

    def padding(self, new_data):
        if self.content.shape[1] > new_data.shape[1]:
            padded = np.zeros((new_data.shape[0], self.content.shape[1]))
            padded[:] = np.NaN
            padded[:new_data.shape[0], :new_data.shape[1]] = new_data
            self.content = np.concatenate((self.content, padded), axis = 0)
        else:
            padded = np.zeros((self.content.shape[0], new_data.shape[1] ))
            padded[:] = np.NaN
            padded[:self.content.shape[0], :self.content.shape[1]] = self.content
            self.content = np.concatenate((padded, new_data), axis = 0)

class NewData(Reader):
    '''process new data'''
    def __init__(self, file_list):
        super().__init__(file_list)
        self.n_trial = len(self.content)
        self.N = self.content[:, 0]
        if len(self.N) == 0:
            raise ValueError("empty data set!")
        self.N = np.array([int(x) for x in self.N])
        self.position = []
        self.width = []
        self.gravity = []
        self.n_left = []
        self.width = []
        self._get_position()
        self._get_additional_info()

    def _get_position(self):
        for (index, N_particle) in enumerate(self.N):
            position = self.content[index, 1: 3 * N_particle + 1]
            self.position.append(position)

    def check_dimension(self):
        if (len(self.position) != self.n_trial or len(self.width) != self.n_trial):
            raise ValueError("content dimensionos don't match")

    def _get_additional_info(self):
        for index,file in enumerate(self.file_list):
            temp = file.split('-')
            self.width += [int(temp[2][1:])/10] * self.lines_per_file[index]
        self.width = [entry for index, entry in enumerate(self.width) if self.deleted[index]]
            



class OldData(NewData):
    '''process old data'''
    #def __init__(self, content):
    #    super().__init__(content)
        
    
    def check_dimension(self):
        super().check_dimension()
        if (len(self.gravity) != self.n_trial or len(self.n_left) != self.n_trial):
            raise ValueError("content dimensionos don't match")

    def _get_additional_info(self):
        self.width = self.content[:, 48]
        self.gravity = self.content[:, 49]
        self.n_left = self.content[:, 46]
        self.width = self.content[:, 48]

