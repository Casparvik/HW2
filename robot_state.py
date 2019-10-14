#!/usr/bin/env python3

import numpy as np


from world_state import WorldState

# Door sensor - needs to now the world state to answer questions
class RobotState:
    def __init__(self):
        self.set_move_left_probabilities( 0.8, 0.1 )
        self.set_move_right_probabilities( 0.8, 0.1 )

        # Where the robot actually is
        self.robot_loc = 0.5


    # Make sure probabilities add up to one
    def set_move_left_probabilities(self, move_left_if_left = 0.8, move_right_if_left = 0.05 ):
        self.prob_move_left_if_left = move_left_if_left
        self.prob_move_right_if_left = move_right_if_left

        # begin homework 2 : problem 2
        # check probabilities are correct
        self.prob_stay_still_left = (1-(self.prob_move_right_if_left+self.prob_move_left_if_left))
        self.bin_left = [self.prob_move_left_if_left, self.prob_move_right_if_left+self.prob_move_left_if_left, (self.prob_move_right_if_left+self.prob_move_left_if_left)+self.prob_stay_still_left]
        #Bin zero is The actual movement, one is opposite and 2 is nowhere
        if self.bin_left[1]>=1:
            raise ValueError('Probabilities Sum to greater than one')

        # end homework 2 : problem 2

    def set_move_right_probabilities(self, move_right_if_right = 0.8, move_left_if_right = 0.05 ):
        self.prob_move_right_if_right = move_right_if_right
        self.prob_move_left_if_right = move_left_if_right

        # begin homework 2 : problem 2
        # check probabilities are correct
        self.prob_stay_still_right = (1 - (self.prob_move_left_if_right + self.prob_move_right_if_right))
        self.bin_right = [self.prob_move_right_if_right, self.prob_move_left_if_right + self.prob_move_right_if_right,(self.prob_move_left_if_right + self.prob_move_right_if_right) + self.prob_stay_still_right]
        if self.bin_right[1]>=1:
            raise ValueError('Probabilities Sum to greater than one')

        # end homework 2 : problem 2


    def adjust_location(self, n_divs):

        div = 1.0 / n_divs
        bin = min( n_divs-1, max(0, np.round( self.robot_loc / div ) ) )
        self.robot_loc = (bin + 0.5) * div

    # Actually move - don't move off of end of hallway
    def _move_(self, step):
        if 0 <= self.robot_loc + step <= 1:
            self.robot_loc += step
        else:
            step = 0
        return step

    # Roll the dice and move
    def move_left(self, step_size):
        # begin homework 2 : problem 2
        # Flip the coin...
        flip = np.random.uniform(0, 1)
        #left bin probability
        bin = self.bin_left
        #print(bin)
        #print(flip)
        bin_indices = np.digitize(flip, bin)
        #print(bin_indices)
        # Determine whether to move left, right, or stay put - use _move_ to actually move
        if bin_indices==0:
            return self._move_(-step_size)
        elif bin_indices==1:
            return self._move_(step_size)
        else:
            return self._move_(0)
        # end homework 2 : problem 3

    # Roll the dice and move
    def move_right(self, step_size):
        # begin homework 2 : problem 2
        # Flip the coin...
        flip = np.random.uniform(0, 1)
        bin = self.bin_right

        bin_indices = np.digitize(flip, bin)

        # Determine whether to move left, right, or stay put - use _move_ to actually move
        if bin_indices == 0:
            return self._move_(step_size)
        elif bin_indices == 1:
            return self._move_(-step_size)
        else:
            return self._move_(0)
        # Determine whether to move left, right, or stay put - use _move_ to actually move
        # end homework 2 : problem 3


if __name__ == '__main__':
    ws = WorldState()

    rs = RobotState()

    # Move far enough to the left and you should stop moving
    print("Checking _Move_ function")
    step_size = 0.1
    for i in range(0,20):
        rs.move_left(step_size)
        if rs.robot_loc < 0 or rs.robot_loc > 1:
            raise ValueError("Robot went off end of left wall")

    # Repeat for right
    for i in range(0,20):
        rs.move_right(step_size)
        if rs.robot_loc < 0 or rs.robot_loc > 1:
            raise ValueError("Robot went off end of right wall")

    # Check that we get our probabilites back (mostly)
    print("Checking move left probabilities")

    count_moved_left = 0
    count_moved_right = 0
    for i in range(0,1000):
        rs.robot_loc = 0.5
        rs.move_left(step_size)
        if rs.robot_loc == 0.5 - step_size:
            count_moved_left += 1
        elif rs.robot_loc == 0.5 + step_size:
            count_moved_right += 1

    prob_count_left = count_moved_left/1000
    prob_count_right = count_moved_right/1000
    if abs( prob_count_left - rs.prob_move_left_if_left ) > 0.1:
        raise ValueError("Probability should be close to {}, is {}".format( prob_count_left, rs.prob_move_left_if_left))
    if abs( prob_count_right - rs.prob_move_right_if_left ) > 0.1:
        raise ValueError("Probability should be close to {}, is {}".format( prob_count_right, rs.prob_move_right_if_left))

    print("Checking move right probabilities")
    count_moved_left = 0
    count_moved_right = 0
    for i in range(0,1000):
        rs.robot_loc = 0.5
        rs.move_right(step_size)
        if rs.robot_loc == 0.5 - step_size:
            count_moved_left += 1
        elif rs.robot_loc == 0.5 + step_size:
            count_moved_right += 1

    prob_count_left = count_moved_left/1000
    prob_count_right = count_moved_right/1000
    if abs( prob_count_left - rs.prob_move_left_if_right ) > 0.1:
        raise ValueError("Probability should be close to {}, is {}".format( prob_count_left, rs.prob_move_left_if_right))
    if abs( prob_count_right - rs.prob_move_right_if_right ) > 0.1:
        raise ValueError("Probability should be close to {}, is {}".format( prob_count_right, rs.prob_move_right_if_right))

    print( "Passed tests")
