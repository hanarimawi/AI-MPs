# geometry.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
# 
# Created by Jongdeog Lee (jlee700@illinois.edu) on 09/12/2018

"""
This file contains geometry functions that relate with Part1 in MP2.
"""

import math
import numpy as np
from const import *

def computeCoordinate(start, length, angle):
    """Compute the end cooridinate based on the given start position, length and angle.

        Args:
            start (tuple): base of the arm link. (x-coordinate, y-coordinate)
            length (int): length of the arm link
            angle (int): degree of the arm link from x-axis to couter-clockwise

        Return:
            End position of the arm link, (x-coordinate, y-coordinate)
    """
    B = angle
    A = 180 - 90 - B
    C = 90
    c = length
    b_y = (c * math.sin(math.radians(B))) / math.sin(math.radians(C))
    a_x = (c * math.sin(math.radians(A))) / math.sin(math.radians(C))
    return (start[0] + a_x, start[1] - b_y)
    pass

def doesArmTouchObstacles(armPos, obstacles):
    """Determine whether the given arm links touch obstacles

        Args:
            armPos (list): start and end position of all arm links [(start, end)]
            obstacles (list): x-, y- coordinate and radius of obstacles [(x, y, r)]

        Return:
            True if touched. False it not.
    """    
    # for obstacle in obstacles:
    #     max_left = obstacle[0] - obstacle[2]
    #     max_right = obstacle[0] + obstacle[2]
    #     max_bottom = obstacle[0] + obstacle[2]
    #     max_top = obstacle[0] - obstacle[2]
    #     for pos in armPos:
    #         if pos[0] >= max_left and pos[0] <= max_right:
    #             return False 
    #         if pos[1] >= max_top and pos[1] <= max_bottom:
    #             return False

    return False

def doesArmTouchGoals(armEnd, goals):
    """Determine whether the given arm links touch goals

        Args:
            armEnd (tuple): the arm tick position, (x-coordinate, y-coordinate)
            goals (list): x-, y- coordinate and radius of goals [(x, y, r)]

        Return:
            True if touched. False it not.
    """
    return False


def isArmWithinWindow(armPos, window):
    """Determine whether the given arm stays in the window

        Args:
            armPos (list): start and end position of all arm links [(start, end)]
            window (tuple): (width, height) of the window

        Return:
            True if all parts are in the window. False it not.
    """
    return True