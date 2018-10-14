import numpy as np
import pygame
import time
from time import time

dankTime = 0
genColTime = 0
checkAssTime = 0
getLcvTime = 0
recurses = 0
def isValid(col, constraint):
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
    all = genCols1(len(rowCons), vals)
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
            if isValid(col, colCons[i]):
                legitCols[i].append(col)
    legitRows = []
    all = genCols1(len(colCons), vals)

    for i in range(len(rowCons)):
        legitRows.append([])
        for row in all:
            sums = {}
            for v in vals:
                if v > 0:
                    sums[v] = 0
            for l in rowCons[i]:
                sums[l[1]]+=l[0]
            if isValid(row, rowCons[i]):
                legitRows[i].append(row)
    return legitCols, legitRows

def genCols1(l, d):
    if l == 1:
        return [[x] for x in d]
    if l ==0:
        return []
    else:
        half = max(1,int(l/2))
        sub1 = genCols1(l-half, d)
        sub2 = genCols1(half,d)

        ret = [y + x for x in sub1 for y in sub2]
        return ret




def genSplits(slots, zeros):
    if slots == 1:
        return [[zeros]]
    sol = []

    for i in range(zeros+1):
        x = genSplits(slots-1, zeros-i)
        for l in x:
            sol.append([i]+l)
    return sol

def genCol(constraint,length):
    base =[]
    for i in range(len(constraint)):
        temp = []
        for j in range(constraint[i][0]):
            temp.append(1)
        if i < len(constraint)-1:
            temp.append(0)
        base.append(temp)
    cols = []
    digits= 0
    for l in base:
        digits+=len(l)
    s = genSplits(len(base)+1, length-digits)
    for i in range(len(s)):
        cols.append([])
        split = s[i]
        for j in range(len(split)):
            cols[i] = cols[i]+ ([0]*split[j])
            if j <len(split)-1:
                cols[i]+=base[j]
    return(cols)

def genCols(constraints):
    rowCons = constraints[0]
    colCons = constraints[1]
    cols = []
    for i in range(len(colCons)):
        cols.append(genCol(colCons[i], len(rowCons)))

    rows = []
    for i in range(len(rowCons)):
        rows.append(genCol(rowCons[i], len(colCons)))

    return cols, rows

'''
def genCols(constraints):
    global genColTime
    rowCons = constraints[0]
    colCons = constraints[1]

    rows = []
    cols = []
    x = []
    for constraint in rowCons:
        i = 0
        for pair in constraint:
            i+=pair[0]
        y = time()
        x.append(genLists(len(colCons), i))
        genColTime+=time()-y
    for i in range(len(x)):
        rows.append([])
        for row in x[i]:
            if isValid(row, rowCons[i]):
                rows[i].append(row)

    x = []
    for constraint in colCons:
        i = 0
        for pair in constraint:
            i+=pair[0]
        y = time()
        x.append(genLists(len(rowCons), i))
        genColTime+=time()-y

    for i in range(len(x)):
        cols.append([])
        for col in x[i]:
            if isValid(col, colCons[i]):
                cols[i].append(col)
    print(rowCons[0], rows[0])
    return cols, rows

def genLists(length, n):
    #print(length,n)
    sol = [[]]
    if n == 0:
        for i in range(length):
            sol[0].append(0)
        return sol
    if n == length:
        for i in range(length):
            sol[0].append(1)
        return sol
    if length == 0:
        return [[]]
    if n > length:
        print('genlists negative')
    sol = []

    i = int(length/2)
    for j in range(i+1):
        if (n-j) > (length - i) or i < 1 or j <0 or (length-i)<1 or (n-j) <0:
            continue
        left = genLists(i,j)
        right = genLists(length-i,n-j)
        for l1 in left:
            for l2 in right:
                if (l1+l2) not in sol:
                    sol.append(l1+l2)
    #print(sol)
    return sol
'''
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
    #print(len(rows))
    for i in range(len(x[0])):
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
                break
            else:
                if j == len(rows[i])-1:
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
        if not isValid(row,rowCons[i]):
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
    assigned = 0
    for l in range(len(cols)):
        if assignment[l] == []:
            mcv.append(len(cols[l]))
        else:
            mcv.append(np.inf)
            assigned +=1
    if recurses%100 == 0:
        print(assigned)
    i = mcv.index(np.min(mcv))

    x = getLcv(constraints.copy(), assignment.copy(), cols[i].copy(), i)
    for val in x:
        temp = assignment.copy()
        temp[i] = val[1]
        if partial_row_checker(temp.copy(), rows):
            b = backtracking(constraints.copy(), temp.copy(), cols.copy(), rows.copy())
            if b != None:
                return b

    return None


#send copy of cols to recursive
def solve(constraints):
    #x = time()
    cols, rows = genCols(constraints)
    #genColTime = time() -x
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
