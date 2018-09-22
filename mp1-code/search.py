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
import heapq

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


#helper function to backtrack a path from the goal state
def getPath(start, state, visited):
    if state.p == start:
      return [start]
    else:
      return getPath(start,visited[str(state.p)+str(state.obj)][0],visited) + [state.p]

def bfs(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    queue = [state(maze.getStart(),maze.getObjectives(),0)]  #holds frontier
    objs = maze.getObjectives()
    visited = {} #entry is str(point)+str(obj): (previous state, best cost to that state)
    savevis = [] #comprehensive list of visited maze locations
    start = maze.getStart()
    done = False
    while not done:

        curr = queue.pop()

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
                queue.insert(0,n)


    return sol, len(savevis)


def dfs(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    return [], 0

class gstate:
    def __init__(self,p,obj,c):
        self.p = p
        self.obj= obj
        self.c = c
    def __lt__(self, other):
        try:
            return manhattan(self.p,self.obj[0]) < manhattan(other.p,other.obj[0])
        except:
            return self


def greedy(maze):
    # TODO: Write your code here
    heap = [gstate(maze.getStart(),maze.getObjectives(),h(maze.getStart(),maze.getObjectives(),0))]
    heapq.heapify(heap)
    objs = maze.getObjectives()
    visited = {} #entry is str(point)+str(obj): (previous state, best cost to that state)
    savevis = []
    start = maze.getStart()
    done = False
    while not done:
        curr = heapq.heappop(heap)
        if curr.p not in savevis:
            savevis.append(curr.p)
        for neighbor in maze.getNeighbors(curr.p[0],curr.p[1]):
            if maze.isValidMove(neighbor[0],neighbor[1]):
                n = gstate(neighbor,curr.obj.copy(),curr.c+1)
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
                heapq.heappush(heap,n)
    return sol, len(savevis)

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

def astar(maze):
    # TODO: Write your code here
    heap = [state(maze.getStart(),maze.getObjectives(),h(maze.getStart(),maze.getObjectives(),0))]
    heapq.heapify(heap)
    objs = maze.getObjectives()
    visited = {} #entry is str(point)+str(obj): (previous state, best cost to that state)
    savevis = [] #comprehensive list of visited maze locations by all paths
    start = maze.getStart()
    done = False
    while not done:
        curr = heapq.heappop(heap)
        if curr.p not in savevis:
            savevis.append(curr.p)
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
                heapq.heappush(heap,n)
    return sol, len(savevis)

'''

        if curr.point in objs:
                print("found obj")
                saveobjs.append(getPath(start,curr.point,visited))
                curr.objs.remove(curr.point)
                if(len(objs)>=1):
                    cobj = objs[0]
                heap = [(manhattan(curr[1],cobj),curr[1])]
                visited = {}
                start = curr[1]
        else:
            if curr[1] not in savevis:
                savevis.append(curr[1])
            for neighbor in maze.getNeighbors(curr[1][0],curr[1][1]):
                if neighbor in visited.keys():
                  if visited[neighbor][0] > curr[0]:
                    visited[neighbor] = ((curr[0]-manhattan(curr[1],cobj)+manhattan(neighbor,cobj)+1),curr[1])
                  if visited[neighbor][0] <= curr[0]:
                    continue
                else:
                    visited[neighbor] = ((curr[0]-manhattan(curr[1],cobj)+manhattan(neighbor,cobj)+1),curr[1])
                if maze.isValidMove(neighbor[0],neighbor[1]):
                    heapq.heappush(heap,(curr[0]-manhattan(curr[1],cobj)+manhattan(neighbor,cobj)+1, neighbor))
    sol = [maze.getStart()]
    for i in range(0, len(saveobjs)):
        for j in range(0,len(saveobjs[i])):
            sol.append(saveobjs[i][j])
            '''
