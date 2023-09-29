import numpy as np
import time

'''
In this code there is a 3D matrix where on it we see "1" number on random indexes. 
There is a "collector" on the matrix who gather this "1"s one by one.

The "collector" begin in this case the gathering on the [0][0][0] index. Where it finished  a matrix, it will be 
location on the next matrix where it  finished previous.

For example:
    If the "collector" finished on the [0][3][2] index, it will be appear on the next matrix at the [1][3][2] index.
    Then the "collector" will be going to the first "1" to further gathering ...
    
If the collector collected all "1"s, the code will be refreshing new "1"s on the boards
'''


class MatrixBoard:  # making matrix class
    def __init__(self, shape_of_array):
        self.array_parameters = shape_of_array  # shape of the array
        self.array = self.generate_elements_on_matrix()

    def generate_elements_on_matrix(self):
        return np.random.randint(0, 2, self.array_parameters)  # create matrix

    def refresh_boards(self):  # refresh the board after the collector collected the numbers
        self.array = np.random.randint(0, 2, self.array_parameters)

    def __str__(self):
        return f'{self.array}'


class Collector:  # collector class
    def __init__(self):
        self.collector_first_idx = 0  # collector first index position on the matrix
        self.collector_second_idx = 0  # collector second index position on the matrix
        self.collector_third_idx = 0  # collector third index position on the matrix

    def forward_movement(self, index, argwhere):  # step forward until the collector found a "1"

        if self.collector_first_idx < argwhere[index][0]:  # step to the next matrix
            self.collector_first_idx += 1
        if self.collector_second_idx < argwhere[index][1] and self.collector_third_idx == argwhere[index][2]:  # step to the next row on the matrix where is the first "1"
            self.collector_second_idx += 1
        if self.collector_third_idx < argwhere[index][2]:  # step to the next column on the row
            self.collector_third_idx += 1

    def backward_movement(self, index, argwhere):
        if self.collector_first_idx > argwhere[index][0]:  # step back on the board
            self.collector_first_idx -= 1
        if self.collector_second_idx > argwhere[index][1]:  # step back over the rows until the collector arrived the correct row
            self.collector_second_idx -= 1
        if self.collector_third_idx > argwhere[index][2]:  # step back over the columns
            self.collector_third_idx -= 1

    def collect_number(self, index, argwhere, board):
        if argwhere[index][0] == self.collector_first_idx and argwhere[index][1] == self.collector_second_idx and \
                argwhere[index][2] == self.collector_third_idx:  # if the collector is on an index where is a "1" ....
            board[self.collector_first_idx][self.collector_second_idx][self.collector_third_idx] = 0  # There will be a "0" instead of "1", because the collector gathered the number ...
            index += 1  # then we are going to the next "1" location in the list of collected indexes of "1".


class SetBoard:  # collection process class
    def __init__(self, array_shape):
        self.board = MatrixBoard(array_shape)  # here we call the create matrix class
        self.collector = Collector()  # here we call the collector matrix
        self.collecting = True

    def collecting_process(self):  # collecting method
        while self.collecting:

            coppied_board = self.board.array.copy()  # copy the original board. In this case we can modify the board status
            list_of_indexes_of_ones = np.argwhere(self.board.array == 1)  # collecting the "ones" index position into a list

            # position of the collector
            coppied_board[self.collector.collector_first_idx][self.collector.collector_second_idx][self.collector.collector_third_idx] = 5

            print(f'\nCollecting ... \n{coppied_board}')

            time.sleep(1)

            # steps of the gathering
            self.steps_of_gathering(list_of_indexes_of_ones)

    def steps_of_gathering(self, argwhere): # steps of the gathering
        index = 0  # counting over the list of gatherable numbers index locations

        if len(argwhere) != 0:  # if there is any "1" on the board
            self.collector.forward_movement(index, argwhere)
            self.collector.backward_movement(index, argwhere)
            self.collector.collect_number(index, argwhere, self.board.array)
        else:  # if all collected....
            self.board.refresh_boards()  # generate new "1"s
            
            
shape = (3, 4, 4)
arr = SetBoard(shape)
arr.collecting_process()

print("Numbers collected.")
