import numpy as np
import time
from copy import deepcopy

'''
In this code there is a 3D matrix where on it we see "1" number on random indexes. 
There is a "collector" on the matrix who gather this "1"s one by one.

The "collector" begin in this case the gathering on the [0][0][0] index. Where it finished  a matrix, it will be 
location on the next matrix where it  finished previous.

For example:
    If the "collector" finished on the [0][3][2] index, it will be appear on the next matrix at the [1][3][2] index.
    Then the "collector" will be going to the first "1" to further gathering ...
If the collector collected all "1"s on the boards, the code will be refreshing new "1"s on the boards.


Then the code will be making a nested list where will be storing the collected '1's. And this nested list will be
in an numpy array .
So we made a 3D array whit different sized cells in a nested list.

And when the collector collected the numbers, it will be move to the end of a created cell where it will be storing the 
collected '1's.

Conclusion:
    The collector movements in the storage is not in the 'Collector' class. So we could overwrite to the 'Collector' 
    class.
    And we could examine how different ways exist to make a 3D array with different shapes.
    
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


class StorageOfTheCollectedNumbers:  # create storage class
    def __init__(self):

        self.collected_amount = 0  # number of collected '1's
        self.length = 0  # length of the cell
        self.col = 2  # width of the cell

        self.storage = []  # Here we store the cells in nested list
        self.storage_in_array = np.array([], dtype=object)  # Here will we store the nested list with the array

        '''
                Here you see how can we make a 3D array with
                different sized arrays in a nested list.
                
                '''

    def collected(self, collected_numbers):  # get the collected amount of '1's
        self.collected_amount = collected_numbers

    def determine_the_shape_of_the_cell(self):  # create the shape of the cell

        if self.collected_amount % 2 == 0:
            self.length = self.collected_amount // 2

        elif self.collected_amount % 2 == 1:
            self.length = self.collected_amount // 2
            self.length += 1

        '''
            For example:
                If the collected amount is even number then: 
                    the length of the cell will be "collected amount // 2"
                    
                    amount_of_ones = 4
                    [[1 1]
                     [1 1]]

                if the collected amount is odd number then:
                    the length of the cell will be "(collected amount // 2) + 1"
                    
                    amount_of_ones = 5
                    [[0 1]
                     [1 1]
                     [1 1]]
             '''

    def fill_storage_with_cell(self):
        self.storage.append(np.zeros((self.length, self.col), dtype=int))  # append the created cell to the storage
        self.storage_in_array = np.array(self.storage, dtype=object)  # then put the nested list into the array

    def make_the_cell(self, collected_numbers):  # make the cell process
        self.collected(collected_numbers)
        self.determine_the_shape_of_the_cell()
        self.fill_storage_with_cell()


class Collector(StorageOfTheCollectedNumbers):  # collector class
    def __init__(self):
        super().__init__()
        self.collector_first_idx = 0  # collector first index position on the matrix
        self.collector_second_idx = 0  # collector second index position on the matrix
        self.collector_third_idx = 0  # collector third index position on the matrix
        self.collected_numbers = 0

    def forward_movement(self, index, argwhere):  # step forward until the collector found a "1"

        if self.collector_first_idx < argwhere[index][0]:  # step to the next matrix
            self.collector_first_idx += 1
        if self.collector_second_idx < argwhere[index][1] and \
           self.collector_third_idx == argwhere[index][2]:  # step to the next row on the matrix where is the first "1"
            self.collector_second_idx += 1
        if self.collector_third_idx < argwhere[index][2]:  # step to the next column on the row
            self.collector_third_idx += 1

    def backward_movement(self, index, argwhere):
        if self.collector_first_idx > argwhere[index][0]:  # step back on the board
            self.collector_first_idx -= 1
        # step back over the rows until the collector arrived the correct row:
        if self.collector_second_idx > argwhere[index][1]:
            self.collector_second_idx -= 1
        if self.collector_third_idx > argwhere[index][2]:  # step back over the columns
            self.collector_third_idx -= 1

    def collect_number(self, index, argwhere, board):
        # There will be a "0" instead of "1", because the collector gathered the number ...
        if argwhere[index][0] == self.collector_first_idx and argwhere[index][1] == self.collector_second_idx and \
                argwhere[index][2] == self.collector_third_idx:  # if the collector is on an index where is a "1" ....
            board[self.collector_first_idx][self.collector_second_idx][
                self.collector_third_idx] = 0
            self.collected_numbers += 1
            index += 1  # then we are going to the next "1" location in the list of collected indexes of "1".


class SetStorage(Collector):
    def __init__(self):
        super().__init__()
        self.load_the_nums = True
        self.lets_get_load = True
        self.jump = False  # flag for jump back a row
        self.first_idx = 0  # collector first index position on the storage cell
        self.second_idx = 0  # collector second index position on the storage cell
        self.third_idx = 0  # collector third index position on the storage cell
        self.len = 1  # for counting the length of the array of storage cell

    def move_to_the_end(self, storage):  # move to the end of the storage cell
        if self.second_idx != len(storage[self.len - 1]) - 1:
            self.second_idx += 1

        if self.third_idx != self.col - 1:
            self.third_idx += 1

    def move_back(self, storage):  # move back to the beginning of the storage cell
        index = len(storage[self.len - 1]) - 1
        if self.third_idx == 1 and self.jump:
            self.third_idx -= 1
            self.jump = False

        if self.second_idx > 0 and self.third_idx == 0 and self.jump:
            self.second_idx -= 1
            self.third_idx += 1
            index -= 1

            self.jump = True

        if self.third_idx == 1 and not self.jump:
            self.third_idx -= 1
            self.jump = True

        if self.third_idx == 0 and not self.jump:
            self.jump = True

    def turn_zeros_to_ones(self, storage, amount):  # turn the zeros to '1' while the collector move back
        if amount > 0:
            storage[self.len - 1][self.second_idx][self.third_idx] = 1

        # handle of what if the collected amount is odd number or even number
        elif amount == 0 and storage[self.len - 1][0][0] == 5:
            storage[self.len - 1][self.second_idx][self.third_idx] = 0
            print("--------------------------------")
            print("\nFill the storage with '1's...")
            print(f'{storage[self.len - 1]}')
            print(f"Remainded '1' s :{amount}")
            self.lets_get_load = False

        if storage[self.len - 1][0][0] == 1:
            print("--------------------------------")
            print("\nFill the storage with '1's...")
            print(f'{storage[self.len - 1]}')
            print(f"Remainded '1' s :{amount}")
            self.lets_get_load = False

    def load_the_collected_numbers(self, storage, collected_amount):  # load the "1"s into the cell process

        while self.lets_get_load:
            # we copied the selected cell from the nested list. In this case we wont override the original
            copied_storage = storage.copy()[self.len - 1]

            copied_storage[self.second_idx][self.third_idx] = 5

            print("--------------------------------")
            print("\nFill the storage with '1's...")
            print(f'{copied_storage}')
            print(f"Remainded '1' s :{collected_amount}")
            self.turn_zeros_to_ones(storage, collected_amount)  # turn the zeros to '1's process in the original cell
            collected_amount -= 1  # count the collected '1's amount
            self.move_back(storage)  # move back process

            time.sleep(1)

        # Reset back the while loop and the movement indexes to zero for
        self.lets_get_load = True
        self.first_idx = 0  # collector first index position on the storage cell
        self.second_idx = 0  # collector second index position on the storage cell
        self.third_idx = 0  # collector third index position on the storage cell

        # counting the nested list cells
        self.len += 1

    def move_to_end_of_the_cell(self, storage):  # move to the end of the cell

        while self.load_the_nums:
            # we copied the selected cell from the array of storage. In this case we wont override the original
            copied_storage = deepcopy(storage)[self.len - 1]
            copied_storage[self.second_idx][self.third_idx] = 5

            self.move_to_the_end(storage)  # move to the end process

            print("--------------------------------")
            print("\nMove to the end of storage...")
            print(copied_storage)

            # if the collector arrived penult cell index
            if self.second_idx == len(storage[self.len - 1]) - 1 and self.third_idx == self.col - 1:
                # Then the last index will be ....
                copied_storage[self.second_idx][self.third_idx] = 5
                # And close the "move to the end of the cell" process
                self.load_the_nums = False

            time.sleep(1)

        # Then turn the "load the nums" flag to True for the next cell while loop
        self.load_the_nums = True


class Collect:  # collection process class
    def __init__(self, array_shape):
        self.board = MatrixBoard(array_shape)  # here we call the create matrix class
        self.collector = Collector()  # here we call the collector matrix
        self.set_storage = SetStorage()
        self.collecting = True

    def collecting_process(self):  # collecting method

        while self.collecting:
            # copy the original board. In this case we can modify the board status
            copied_board = self.board.array.copy()

            list_of_indexes_of_ones = np.argwhere(
                self.board.array == 1)  # collecting the "ones" index position into a list

            # position of the collector
            copied_board[self.collector.collector_first_idx][self.collector.collector_second_idx][
                self.collector.collector_third_idx] = 5

            print(f'\nCollecting ... \n{copied_board}')
            print(f'\n Collected numbers: {self.collector.collected_numbers}')

            time.sleep(1)

            # steps of the gathering
            self.steps_of_gathering(list_of_indexes_of_ones)

            # steps of the loading into storage
            self.loading_to_storage_progress(list_of_indexes_of_ones)

    def steps_of_gathering(self, argwhere):  # steps of the gathering
        index = 0  # counting over the list of gatherable numbers index locations

        if len(argwhere) != 0:  # if there is any "1" on the board

            self.collector.forward_movement(index, argwhere)
            self.collector.backward_movement(index, argwhere)
            self.collector.collect_number(index, argwhere, self.board.array)
        else:  # if all collected....

            self.board.refresh_boards()  # generate new "1"s
            self.collector.make_the_cell(self.collector.collected_numbers)
            self.collector.collected_numbers = 0

            print("--------------------------------")
            print(f'\nHere is the array of Storage:')
            print(f'{self.collector.storage_in_array}')
            time.sleep(2)

    def loading_to_storage_progress(self, list_of_indexes_of_ones):  # steps of loading
        if len(list_of_indexes_of_ones) == 0:
            self.set_storage.move_to_end_of_the_cell(self.collector.storage_in_array)
            self.set_storage.load_the_collected_numbers(self.collector.storage, self.collector.collected_amount)


shape = (3, 4, 4)
arr = Collect(shape)
arr.collecting_process()
