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
    adjacent = length * math.cos(math.radians(angle))
    opposite = length * math.sin(math.radians(angle))
    return start[0] + adjacent, start[1] - opposite

def getD(p1,p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def getSlope(p1,p2):
    if p1[0]==p2[0]:
        return np.inf
    if p2[0] > p1[0]:
        return (p2[1]-p1[1])/(p2[0]-p1[0])
    else:
        return (p1[1]-p2[1])/(p1[0]-p2[0])
def doesArmTouchObstacles(armPos, obstacles):
    """Determine whether the given arm links touch obstacles

        Args:
            armPos (list): start and end position of all arm links [(start, end)]
            obstacles (list): x-, y- coordinate and radius of obstacles [(x, y, r)]

        Return:
            True if touched. False it not.

    Ex:
    pos:  [((150, 200), (150.0, 100.0)), ((150.0, 100.0), (106.69872981077808, 75.0))] 
    obs:  [(125, 70, 10),(90, 90, 10), (165, 30, 10), (185, 60, 10)]
    """    
    for obstacle in obstacles:
        for arm_tick in armPos:
            y_1 = arm_tick[0][1] * -1
            y_2 = arm_tick[1][1] * -1
            x_1 = arm_tick[0][0]
            x_2 = arm_tick[1][0]
            a = y_1 - y_2
            b = x_2 - x_1
            c = (x_1 * y_2) - (x_2 * y_1)
            x = obstacle[0]
            y = obstacle[1] * -1
            dist = ( (abs(a * x + b * y + c)) / math.sqrt(a * a + b * b))  
            obs = (obstacle[0], y)
            arm_2 = (x_2, y_2)
            arm_1 = (x_1, y_1)
            print("dist: ", dist)
            max_d = max(getD(arm_1, obs), getD(arm_2, obs))
            if getSlope(arm_1,arm_2) == getSlope(arm_2, obs) or max_d > getD(arm_1, arm_2):
                d1 = getD(arm_1, obs)
                d2 = getD(arm_2, obs)
                min_d = min(d1, d2)
                if min_d < obstacle[2]:
                    print("AYYYY")
                    return True 
            elif dist <= obstacle[2]:
                print("dist: "  , dist) # " obstacle: ( ", obstacle[0], " , ", obstacle[1], " ) "
                return True
    return False


def doesArmTouchGoals(armEnd, goals):
    """Determine whether the given arm links touch goals

        Args:
            armEnd (tuple): the arm tick position, (x-coordinate, y-coordinate)
            goals (list): x-, y- coordinate and radius of goals [(x, y, r)]

        Return:
            True if touched. False it not.
    """
    for goal in goals:
            a = armEnd[0] - goal[0]
            b = armEnd[1] - goal[1]
            c = math.sqrt((a**2 + b**2))
            if goal[2] >= c:
                return True
    return False


def isArmWithinWindow(armPos, window):
    """Determine whether the given arm stays in the window

        Args:
            armPos (list): start and end position of all arm links [(start, end)]
            window (tuple): (width, height) of the window

        Return:
            True if all parts are in the window. False it not.

    Ex:
    pos:  [((150, 200), (150.0, 100.0)), ((150.0, 100.0), (106.69872981077808, 75.0))] 
    """
    for pos in armPos:
        if pos[0][0] < 0 or pos[0][0] > window[0]:
            return False
        if pos[0][1] < 0 or pos[0][1] > window[1]:
            return False
        if pos[1][0] < 0 or pos[1][0] > window[0]:
            return False
        if pos[1][1] < 0 or pos[1][1] > window[1]:
            return False
    return True
