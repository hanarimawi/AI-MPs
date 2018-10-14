import numpy as np
import pygame
import time
from time import time

dankTime = 0
genColTime = 0
checkAssTime = 0
getLcvTime = 0
recurses = 0
def isDank(col, constraint, sums):
    x = time()
    curr = [0,0]
    sol = []
    for i in range(len(col)):
        if col[i] == 0:
            if curr[0] > 0:
                sol.append(curr)
            curr = [0,0]
            continue
        if curr[1] == 0:
            curr[1] = col[i]
            curr[0] = 1
        else:
            curr[0]+=1
    if col[len(col)-1] != 0:
        sol.append(curr)
    global dankTime
    dankTime+=time()-x
    if sol == constraint:
        return True
    else:
        return False

def getCols(constraints):
    vals = [0]
    colCons = constraints[1]
    rowCons = constraints[0]
    for c in rowCons+colCons:
        for l in c:
            if l[1] not in vals:
                vals.append(l[1])
    all = genCols(len(rowCons), vals)
    legitCols = []
    for i in range(len(colCons)):
        legitCols.append([])
        for col in all:
            sums = {}
            for v in vals:
                if v > 0:
                    sums[v] = 0
            for l in colCons[i]:
                sums[l[1]]+=l[0]
            if isDank(col, colCons[i], sums):
                legitCols[i].append(col)
    legitRows = []
    all = genCols(len(colCons), vals)
    #print(all)
    #print(vals)
    #print(rowCons)
    for i in range(len(rowCons)):
        legitRows.append([])
        for row in all:
            sums = {}
            for v in vals:
                if v > 0:
                    sums[v] = 0
            for l in rowCons[i]:
                sums[l[1]]+=l[0]
            if isDank(row, rowCons[i], sums):
                legitRows[i].append(row)
    return legitCols, legitRows

def genCols(l, d):
    if l == 1:
        return [[x] for x in d]
    if l ==0:
        return []
    else:
        half = max(1,int(l/2))
        sub1 = genCols(l-half, d)
        sub2 = genCols(half,d)

        ret = [y + x for x in sub1 for y in sub2]
        return ret



def partial_row_checker(assignment, rows):
    """
    assume cols is 2d array and constraints is list([[1, 1], [1, 1], [1, 1]])
    return whether the columns are viable given the row constraints
    """
    for i in range(len(assignment)):
        if assignment[i] == []:
            assignment[i] = [-1]*len(rows)

    #print(rows)

    x = np.array(assignment)
    print(x)
    #print(len(rows))
    for i in range(len(x[0])):
        print(rows[i])
        for j in range(len(rows[i])):
            match = True
            for k in range(len(x)):
                if x[k][i] == -1:
                    continue
                if x[k][i] != rows[i][j][k]:
                    #print(x[k])
                    #print(rows[i][j])
                    match = False
            if match:
                continue
            else:
                if k == len(x)-1:
                    return False

    return True

#i is the row
#j is the index of possible row
#k is the column

def checkAss(constraints, assignment):
    x = time()
    global checkAssTime

    rowCons = constraints[0]
    for i in range(len(assignment[0])):
        row = []
        for j in range(len(assignment)):
            row.append(assignment[j][i])

        for l in rowCons[i]:
            sums = {}
            if l == []:
                continue
            if l[1] in sums.keys():
                sums[l[1]]+=l[0]
            else:
                sums[l[1]]=l[0]
        if not isDank(row,rowCons[i],sums):
            checkAssTime+=time()-x
            return False
    checkAssTime+=time()-x
    return True


def getLcv(constraints, assignment, cols, coli):
    x = time()
    rowSums = []
    vals = []
    rowCons = constraints[0]
    for i in range(len(rowCons)):
        rowSums.append(0)
        for j in rowCons[i]:
            rowSums[i] += j[0]
    colSums = []
    for i in range(len(cols)):
        count = 0
        for j in range(len(cols[i])):
            if cols[i][j] == 1:
                count+=rowSums[j]
        colSums.append((count,cols[i]))
    colSums.sort(reverse=True)
    global getLcvTime
    getLcvTime+=time()-x
    return colSums


def backtracking(constraints, assignment, cols,rows):
    print(assignment)
    global recurses
    recurses+=1
    if recurses%500 == 0:
        print(recurses)
    if [] not in assignment:
        if checkAss(constraints, assignment):
            return assignment
        else:
            return None
    mcv = []
    rowCons = constraints[0]
    colCons = constraints[1]
    for l in range(len(cols)):
        if assignment[l] == []:
            mcv.append(len(cols[l]))
        else:
            mcv.append(np.inf)
    i = mcv.index(np.min(mcv))
    x = getLcv(constraints.copy(), assignment.copy(), cols[i].copy(), i)
    for val in x:
        temp = assignment.copy()
        temp[i] = val[1]
        if partial_row_checker(temp, rows):
            b = backtracking(constraints.copy(), temp.copy(), cols.copy(), rows.copy())
            if b != None:
                return b

    return None


#send copy of cols to recursive
def solve(constraints):
    x = time()
    cols, rows = getCols(constraints)
    genColTime = time() -x
    colCons = constraints[1]
    rowCons = constraints[0]
    a= []
    for i in range(len(colCons)):
        a.append([])
    print(len(colCons))
    print('begin backtracking')

    x = backtracking(constraints, a, cols,rows)
    x = np.array(x)
    x = np.transpose(x)
    print(dankTime,genColTime,checkAssTime,getLcvTime)
    print(x)
    return np.array(x)



    """
    Implement me!!!!!!!
    This function takes in a set of constraints. The first dimension is the axis
    to which the constraints refer to. The second dimension is the list of constraints
    for some axis index pair. The third demsion is a single constraint of the form
    [i,j] which means a run of i js. For example, [4,1] would correspond to a block
    [1,1,1,1].

    The return value of this function should be a numpy array that satisfies all
    of the constraints.


    A puzzle will have the constraints of the following format:


    array([
        [list([[4, 1]]),
         list([[1, 1], [1, 1], [1, 1]]),
         list([[3, 1], [1, 1]]),
         list([[2, 1]]),
         list([[1, 1], [1, 1]])],
        [list([[2, 1]]),
         list([[1, 1], [1, 1]]),
         list([[3, 1], [1, 1]]),
         list([[1, 1], [1, 1]]),
         list([[5, 1]])]
        ], dtype=object)

    And a corresponding solution may be:

    array([[0, 1, 1, 1, 1],
           [1, 0, 1, 0, 1],
           [1, 1, 1, 0, 1],
           [0, 0, 0, 1, 1],
           [0, 0, 1, 0, 1]])



    Consider a more complicated set of constraints for a colored nonogram.

    array([
       [list([[1, 1], [1, 4], [1, 2], [1, 1], [1, 2], [1, 1]]),
        list([[1, 3], [1, 4], [1, 3]]),
        list([[1, 2]]),
        list([[1, 4], [1, 1]]),
        list([[2, 2], [2, 1], [1, 3]]),
        list([[1, 2], [1, 3], [1, 2]]),
        list([[2, 1]])],
       [list([[1, 3], [1, 4], [1, 2]]),
        list([[1, 1], [1, 4], [1, 2], [1, 2], [1, 1]]),
        list([[1, 4], [1, 1], [1, 2], [1, 1]]),
        list([[1, 2], [1, 1]]),
        list([[1, 1], [2, 3]]),
        list([[1, 2], [1, 3]]),
        list([[1, 1], [1, 1], [1, 2]])]],
        dtype=object)

    And a corresponding solution may be:

    array([
           [0, 1, 4, 2, 1, 2, 1],
           [3, 4, 0, 0, 0, 3, 0],
           [0, 2, 0, 0, 0, 0, 0],
           [4, 0, 0, 0, 0, 0, 1],
           [2, 2, 1, 1, 3, 0, 0],
           [0, 0, 2, 0, 3, 0, 2],
           [0, 1, 1, 0, 0, 0, 0]
         ])


    """
