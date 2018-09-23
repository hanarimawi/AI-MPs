# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
# 
# Created by Michael Abir (abir2@illinois.edu) on 08/28/2018
import heapq

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

def getPath(start, state, visited):
    if state.p == start:
      return [start]
    else:
      return getPath(start,visited[str(state.p)+str(state.obj)][0],visited) + [state.p]

def dfs(maze):
    stack = [state(maze.getStart(),maze.getObjectives(),0)]  #holds frontier
    objs = maze.getObjectives()
    visited = {} #entry is str(point)+str(obj): (previous state, best cost to that state)
    savevis = [] #comprehensive list of visited maze locations
    start = maze.getStart()
    done = False
    while not done:

        curr = stack.pop()

        if curr.p not in savevis:
          savevis.append(curr.p)

        #process each neighbor and check if we've reached the goal
        for neighbor in maze.getNeighbors(curr.p[0],curr.p[1]):
            if maze.isValidMove(neighbor[0],neighbor[1]):
                n = state(neighbor,curr.obj.copy(),curr.c+1)
                if neighbor in n.obj:
                    n.obj.remove(neighbor)
                skey = str(n.p)+str(n.obj)
                if skey in visited.keys():
                    if visited[skey][1] > n.c:
                        visited[skey] = (curr,n.c)
                    if visited[skey][1] <= n.c:
                        continue
                else:
                    visited[skey] = (curr,n.c)
                if len(n.obj) == 0:
                    sol = getPath(maze.getStart(),n,visited)
                    done = True
                stack.insert(0, n)#.append(n)
    return sol, len(savevis)

def greedy(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    return [], 0


def astar(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    return [], 0

def manhattan(p1,p2):
    return abs(p1[0]-p2[0])+abs(p1[1]-p2[1])

def h(point, obj,cost):
    if len(obj) == 0:
        return cost
    z = max([manhattan(point, i) for i in obj])
    y= []
    z = 0
    for i in range(len(obj)-1):
        d = [manhattan(point, i) for i in obj]
        if 0 in d:
            d.remove(0)
        z+=(min(d))
        z = sum(y)
    return z + cost

class state:
    def __init__(self,p,obj,c):
        self.p = p
        self.obj= obj
        self.c = c
    def __lt__(self, other):
        return self.c + h(self.p,self.obj,self.c) < other.c + h(other.p,other.obj,other.c)
