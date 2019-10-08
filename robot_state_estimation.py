#!/usr/bin/env python3

import numpy as np

from world_state import WorldState
from door_sensor import DoorSensor
from robot_state import RobotState


# Belief about world/robot state
class RobotStateEstimation:
    def __init__(self):

        # Probability representation (discrete)
        self.reset_probabilities(10)

    def reset_probabilities(self, n_probability):
        """ Initialize discrete probability resolution with uniform distribution """
        div = 1.0 / n_probability
        self.probabilities = np.ones(n_probability) * div

    def update_belief_sensor_reading(self, ws, ds, sensor_reading_has_door):
        """ Update your probabilities based on the sensor reading being true (door) or false (no door)
        :param ws World state - has where the doors are
        :param ds Door Sensor - has probabilities for door sensor readings
        :param sensor_reading_has_door - returns true/false if in front of door
        """
        print("Update sensor, reading {}".format(sensor_reading_has_door))

        # begin homework 2 : problem 3

        n = 0
        new_prob = np.zeros(ws.n_bins)
        bin_size = 1 / ws.n_bins
        half_bin = bin_size / 2
        for j in range(0, ws.n_bins):
            if ws.is_in_front_of_door((j * bin_size) + half_bin):
                if sensor_reading_has_door:
                    new_prob[j] = (ds.prob_see_door_if_door) * self.probabilities[j]
                else:
                    new_prob[j]= (1-ds.prob_see_door_if_door) * self.probabilities[j]
            else:
                if sensor_reading_has_door == False:
                    new_prob[j] = ( 1 - ds.prob_see_door_if_no_door)*self.probabilities[j]
                else:
                    new_prob[j] = (ds.prob_see_door_if_no_door) * self.probabilities[j]

            n = n + new_prob[j]


        for j in range(0, ws.n_bins):
            new_prob[j] = new_prob[j] / n

        self.probabilities = new_prob

        # Normalize - all the denominators are the same
        # end homework 2 : problem 3

    def update_belief_move_left(self, rs,n_divs):
        """ Update the probabilities assuming a move left.
        :param rs - robot state, has the probabilities"""

        # begin homework 2 problem 4
        new_probs = np.zeros(n_divs)
        left_edge = 0
        right_edge = n_divs-1
        # Check probability of left, no, right sum to one
        for i in range(0, n_divs):
            sum=0
            if i == left_edge:
                sum += rs.prob_move_left_if_left*self.probabilities[left_edge]
                sum += rs.prob_stay_still_left*self.probabilities[i]
                sum += rs.prob_move_left_if_left*self.probabilities[left_edge+1]
            elif i == right_edge:
                sum += rs.prob_move_right_if_left * self.probabilities[right_edge]
                sum += rs.prob_stay_still_left * self.probabilities[i]
            else:
                sum += rs.prob_move_left_if_left*self.probabilities[i+1]
                sum += rs.prob_stay_still_left*self.probabilities[i]
                sum += rs.prob_move_right_if_left*self.probabilities[i-1]


            new_probs[i] = sum
        self.probabilities=new_probs

        # Left edge - put move left probability into zero square along with stay-put probability
        # Right edge - put move right probability into last square
        # Normalize - sum should be one, except for numerical rounding


        sum_prob = np.sum(self.probabilities)
        if abs(sum_prob - 1) > 0.0001:
            ValueError("Sum of probabilities should be 1, is {}".format(sum_prob))
        # end homework 2 problem 4

    def update_belief_move_right(self, rs,n_divs):
        """ Update the probabilities assuming a move right.
        :param rs - robot state, has the probabilities"""
        new_probs = np.zeros(n_divs)
        left_edge = 0
        right_edge = n_divs - 1
        # Check probability of left, no, right sum to one
        for i in range(0, n_divs):
            sum = 0
            if i == left_edge:
                sum += rs.prob_move_left_if_right * self.probabilities[left_edge]
                sum += rs.prob_stay_still_right * self.probabilities[i]

            elif i == right_edge:
                sum += rs.prob_move_right_if_right * self.probabilities[right_edge]#Bounce
                sum += rs.prob_stay_still_right * self.probabilities[i]
                sum += rs.prob_move_right_if_right * self.probabilities[right_edge - 1]
            else:
                sum += rs.prob_move_left_if_right * self.probabilities[i + 1]
                sum += rs.prob_stay_still_right * self.probabilities[i]
                sum += rs.prob_move_right_if_right * self.probabilities[i - 1]

            new_probs[i] = sum
        self.probabilities = new_probs
        # begin homework 2 problem 4
        # Check probability of left, no, right sum to one
        # Left edge - put move left probability into zero square along with stay-put probability
        # Right edge - put move right probability into last square
        # Normalize - sum should be one, except for numerical rounding
        sum_prob = np.sum(self.probabilities)
        if abs(sum_prob - 1) > 0.0001:
            ValueError("Sum of probabilities should be 1, is {}".format(sum_prob))
        # end homework 2 problem 4


if __name__ == '__main__':
    ws = WorldState()

    ds = DoorSensor()

    rse = RobotStateEstimation()

    # Check out these cases
    # We have two possibilities - either in front of door, or not - cross two sensor readings
    #   saw door versus not saw door
    uniform_prob = rse.probabilities[0]
    # begin homework 2 problem 4
    # Four cases - based on default door probabilities of
    # DoorSensor.prob_see_door_if_door = 0.8
    # DoorSensor.prob_see_door_if_no_door = 0.2
    #  and 10 probability divisions
    # Check that our probabilities are updated correctly
    # end homework 2 problem 4

    print("Passed tests")
