# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
# 
# Created by Michael Abir (abir2@illinois.edu) on 08/28/2018

"""
This is the main entry point for MP1. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
# Search should return the path and the number of states explored.
# The path should be a list of tuples in the form (row, col) that correspond
# to the positions of the path taken by your search algorithm.
# Number of states explored should be a number.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,greedy,astar)

def search(maze, searchMethod):    
    return {
        "bfs": bfs,
        "dfs": dfs,
        "greedy": greedy,
        "astar": astar,
    }.get(searchMethod)(maze)
   

def bfs(maze):
    # 
    return [], 0


from collections import deque

def dfs(maze):
    start = maze.getStart()
    goals = maze.getObjectives()
    num_goals = len(goals)
    visited_goals = []
    path = []
    visited, stack = [], [start]
    num_states_explored = 0
    while stack:
        vertex = stack.pop()
        if (vertex in goals) and (vertex not in visited_goals) :
            visited_goals.append(vertex)
            if len(visited_goals) >= num_goals:
                return path, num_states_explored
        if vertex not in visited:
            path.append(vertex)
            visited.append(vertex)
            num_states_explored += 1
            neighbors = maze.getNeighbors(vertex[0], vertex[1])
            for neighbor in neighbors:
                stack.append(neighbor)
    return path, num_states_explored


def greedy(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    return [], 0


def astar(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    return [], 0
