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
    print(maze.getStart())
    print(maze.getDimensions())
    print(maze.getObjectives())
    return {
        "bfs": bfs(maze),
        "dfs": dfs(maze),
        "greedy": greedy(maze),
        "astar": astar(maze),
    }.get(searchMethod, [])

dirs = [(0,1),(0,-1),(1,0),(-1,0)]
def bfs(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    queue = [[maze.getStart()]]
    objs = maze.getObjectives()
    saveobjs = []
    visited = []
    savevis = []
    while len(objs) > 0:
        curr = queue.pop()
        for neighbor in maze.getNeighbors(curr[len(curr)-1][0],curr[len(curr)-1][1]):
            if neighbor in visited:
                continue
            else:
                visited.insert(0,neighbor)
            temp = curr.copy()
            temp.append(neighbor)
            if neighbor in objs:
                saveobjs.append(temp)
                objs.remove(neighbor)
                queue = [[neighbor]]
                for point in visited:
                    if point not in savevis:
                        savevis.append(point)
                visited = []
            else:
                if maze.isValidMove(neighbor[0],neighbor[1]):
                    queue.insert(0,temp)

    #print(visited)
    sol = []
    for i in range(0, len(saveobjs)):
        for j in range(0,len(saveobjs[i])):
            if i==0 or j >0:
                sol.append(saveobjs[i][j])

    return sol, len(savevis)


def dfs(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    return [], 0


def greedy(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    return [], 0


def astar(maze):
    # TODO: Write your code here

    return [], 0
