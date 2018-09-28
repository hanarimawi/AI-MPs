
# transform.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
# 
# Created by Jongdeog Lee (jlee700@illinois.edu) on 09/12/2018

"""
This file contains the transform function that converts the robot arm map
to the maze.
"""
import copy
from arm import Arm
from maze import Maze
from search import *
from geometry import *
from const import *
from util import *

def transformToMaze(arm, goals, obstacles, window, granularity):
    """This function transforms the given 2D map to the maze in MP1.
    
        Args:
            arm (Arm): arm instance
            goals (list): [(x, y, r)] of goals
            obstacles (list): [(x, y, r)] of obstacles
            window (tuple): (width, height) of the window
            granularity (int): unit of increasing/decreasing degree for angles

        Return:
            Maze: the maze instance generated based on input arguments.

    """
    arm_limits = arm.getArmLimit()
    rows = int(((arm_limits[0][1] - arm_limits[0][0])/granularity) + 1)
    cols = int(((arm_limits[1][1] - arm_limits[1][0])/granularity) + 1 )
    maze = [[SPACE_CHAR]* cols for i in range(rows)]
    alpha_min = arm_limits[0][0]
    start_pos = arm.getArmAngle()
    for r_ind in range(rows): #alpha
        beta_min = arm_limits[1][0]
        for c_ind in range(cols): #beta
            if r_ind == 38 and c_ind == 92:
                print("AYYY")
            arm.setArmAngle((alpha_min, beta_min))
            arm_positions = arm.getArmPos()
            if not isArmWithinWindow(arm_positions, window):
                maze[r_ind][c_ind] = WALL_CHAR
            elif doesArmTouchObstacles(arm_positions, obstacles):
                maze[r_ind][c_ind] = WALL_CHAR
            elif doesArmTouchGoals(arm.getEnd(), goals):
                maze[r_ind][c_ind] = OBJECTIVE_CHAR
            beta_min += granularity
        alpha_min += granularity
    maze[start_pos[0]][start_pos[1]] = START_CHAR
    return Maze(maze, [arm_limits[0][0], arm_limits[1][0]], granularity)