#!/usr/bin/env python3

import numpy as np

from world_state import WorldState
from robot_state import RobotState

# Door sensor - needs to now the world state to answer questions
class DoorSensor:
    def __init__(self):
        self.prob_see_door_if_door = 0.8
        self.prob_see_door_if_no_door = 0.2

    # ground truth
    def is_in_front_of_door(self, ws, rs):
        """
        return ground truth
        :param ws: world state (has doors)
        :param rs: robot state (has robot location)
        :return:
        """
        # Just call world state function with robot_loc
        return ws.is_in_front_of_door(rs.robot_loc)

    # Roll the dice and return sensor value
    def sensor_reading(self, ws, rs):
        """
        Generate a sensor reading using probabilities
        :param ws: world state (has doors)
        :param rs: robot state (has robot location)
        :return:
        """
        # begin homework 2 : problem 1
        flip = np.random.uniform(0,1)
        if ws.is_in_front_of_door(rs.robot_loc) == True:
            bin=[self.prob_see_door_if_door,self.prob_see_door_if_door+ (1-self.prob_see_door_if_door)]
            bin_indices = np.digitize(flip, bin)

        else:
            bin = [self.prob_see_door_if_no_door,self.prob_see_door_if_no_door+(1-self.prob_see_door_if_no_door)]
            bin_indices = np.digitize(flip, bin)


        print(bin_indices)

        if bin_indices == 0:
            return True
        else:
            return False
        # end homework 2 : problem 1

    # set the probabilities based on the gui
    def set_probabilities(self, in_prob_see_door_if_door, in_prob_see_door_if_not_door):
        self.prob_see_door_if_door = in_prob_see_door_if_door
        self.prob_see_door_if_no_door = in_prob_see_door_if_not_door

if __name__ == '__main__':
    ws = WorldState()

    ds = DoorSensor()

    rs = RobotState()

    # Robot should be at 0.5, no door at 0.5, so this should be false
    print("Testing probabilities for robot NOT in front of door")
    rs.robot_loc = ws.place_robot_NOT_in_front_of_door()
    if ds.is_in_front_of_door(ws, rs):
        raise ValueError("The robot should NOT be in front of a door")

    # Check that we get our probabilites back (mostly)
    count_returned_true = 0
    for i in range(0,1000):
        if ds.sensor_reading(ws, rs) == True:
            count_returned_true += 1

    prob_count = count_returned_true/1000
    if abs( prob_count - ds.prob_see_door_if_no_door ) > 0.1:
        raise ValueError("Probability should be close to {}, is {}".format( prob_count, ds.prob_see_door_if_no_door))

    print("Testing probabilities for robot in front of door")
    rs.robot_loc = ws.place_robot_in_front_of_door( )
    if ds.is_in_front_of_door(ws, rs) == False:
        raise ValueError("The robot SHOULD be in front of a door")

    # Check that we get our probabilites back (mostly) when in front of the door
    count_returned_true = 0
    for i in range(0, 1000):
        if ds.sensor_reading(ws, rs) == True:
            count_returned_true += 1

    prob_count = count_returned_true / 1000
    if abs(prob_count - ds.prob_see_door_if_door) > 0.1:
        raise ValueError("Probability should be close to {}, is {}".format(prob_count, ds.prob_see_door_if_door))

    print( "Passed tests")
