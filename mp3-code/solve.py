import numpy as np
import time
from time import time
import copy
import re

dankTime = 0
genColTime = 0
checkAssTime = 0
getLcvTime = 0
partialTime = 0
recurses = 0
partialCalled = 0



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
    x  = time()
    colCons = constraints[1]
    rowCons = constraints[0]
    cols = []
    for i in range(len(colCons)):
        cols.append(genCol(colCons[i], len(rowCons)))
    print("time:", time()-x)
    return cols


def experimental_row_check(assignment, constraints):
    row_constraints = constraints[0]
    dim0 = len(row_constraints)
    for i in range(len(assignment)):
        if assignment[i] == []:
            assignment[i] = [2] * dim0

    for i in range(dim0):
        constraint = row_constraints[i]
        row_col = []
        for j in range(len(assignment)):
            row_col.append(assignment[j][i])
        stringed_row = "".join(map(str, row_col))
        regex = "^(0|2)*"
        for cons in constraint:
            regex = regex + "(1|2){" + str(cons[0]) + "}(0|2)+"
        regex = regex[:-1] + "*$"
        pattern = re.compile(regex)
        if not bool(pattern.match(stringed_row)):
            return False, i
    return True, -1



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


def eliminate_cols(assignment, cols, constraints):
    fail_list = []
    for l in range(len(cols)):
        if assignment[l] == []:
            fail_row = []
            for c in range(len(cols[l])):
                ccond = False
                for r in fail_row:
                    if cols[l][c][r[0]] == r[1]:
                        fail_list.append((l, c))
                        ccond = True
                        break
                if ccond:
                    continue
                temp = copy.deepcopy(assignment)
                temp[l] = cols[l][c]
                global partialCalled
                partialCalled += 1
                cond, row = experimental_row_check(copy.deepcopy(temp), constraints)
                if not cond:
                    fail_list.append((l, c))
                    fail_row.append((row, cols[l][c][row]))
    return fail_list


def backtracking(constraints, assignment, cols):
    global recurses
    sum = 0
    recurses += 1
    for i in range(len(cols)):
        sum += len(cols[i])
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
    if recurses%10 == 0:
        print(assigned, sum)
    i = mcv.index(np.min(mcv))

    x = getLcv(copy.deepcopy(constraints), copy.deepcopy(assignment), copy.deepcopy(cols[i]), i)
    for val in x:
        temp = copy.deepcopy(assignment)
        temp[i] = val[1]

        fail_list = eliminate_cols(temp, cols, constraints)
        elim_cols = copy.deepcopy(cols)
        for tup in fail_list:
            elim_cols[tup[0]][tup[1]] = []
        new_cols = []
        for c in elim_cols:
            new_cols.append([a for a in c if a != []])
        b = backtracking(constraints, temp, new_cols)
        if b:
            return b

    return None


#send copy of cols to recursive
def solve(constraints):
    sum = 0
    y = time()
    cols = genCols(constraints)
    genColTime = time() -y
    colCons = constraints[1]
    rowCons = constraints[0]
    a = []
    for i in range(len(colCons)):
        a.append([])
    print('begin backtracking')
    for i in range(len(cols)):
        sum += len(cols[i])
    x = backtracking(constraints, a, cols)
    x = np.array(x)
    x = np.transpose(x)
    print(partialTime,genColTime,checkAssTime,getLcvTime)
    print(x)
    print("runtime: "+str(time()-y))
    print("partial check calls:" + str(partialCalled))
    print("total amount of column possibilities: " + str(sum))
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
