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
from queue import PriorityQueue

def search(maze, searchMethod):    
    return {
        "bfs": bfs,
        "dfs": dfs,
        "greedy": greedy,
        "astar": astar,
    }.get(searchMethod)(maze)
   

def get_manhattan(currentState, goalState):
    return abs(currentState[0] - goalState[0]) + abs(currentState[1] - goalState[1])


def bfs(maze):
    # 
    return [], 0


def dfs(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    return [], 0


def greedy(maze):
    # TODO: Write your code here
    pq = PriorityQueue()
    start = maze.getStart()
    goal = maze.getObjectives()[0]
    pq.put((get_manhattan(start, goal), start, (-1, -1)))
    visited = {}
    states_seen = 0
    path = list()
    latest = ()
    while not pq.empty():
        current = pq.get()
        states_seen += 1
        visited[current[1]] = current[2]
        if current[1] == goal:
            latest = current[1]
            break
        else:
            for neighbor in maze.getNeighbors(current[1][0], current[1][1]):
                if neighbor not in visited:
                    visited[neighbor[1]] = current[2]
                    pq.put((get_manhattan(neighbor, goal), neighbor, current[1]))
    while latest != (-1, -1):
        path.append(latest)
        latest = visited[latest]
    return path[::-1], states_seen


def astar(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    return [], 0
